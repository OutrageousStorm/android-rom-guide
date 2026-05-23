package main

import (
	"crypto/sha256"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type RomVerification struct {
	Filename string
	LocalSum string
	RemoteSum string
	Valid    bool
}

func calculateSHA256(filepath string) (string, error) {
	file, err := os.Open(filepath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", hash.Sum(nil)), nil
}

func fetchRemoteChecksum(checksumURL string) (string, error) {
	resp, err := http.Get(checksumURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	return strings.TrimSpace(string(body)), nil
}

func verifyRom(romPath, checksumURL string) (*RomVerification, error) {
	filename := filepath.Base(romPath)

	// Calculate local checksum
	localSum, err := calculateSHA256(romPath)
	if err != nil {
		return nil, fmt.Errorf("failed to calculate local checksum: %v", err)
	}

	// Fetch remote checksum
	remoteSum, err := fetchRemoteChecksum(checksumURL)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch remote checksum: %v", err)
	}

	// Compare (handle multi-line checksum files)
	remoteSum = strings.Fields(remoteSum)[0]

	verification := &RomVerification{
		Filename:  filename,
		LocalSum:  localSum,
		RemoteSum: remoteSum,
		Valid:     strings.EqualFold(localSum, remoteSum),
	}

	return verification, nil
}

func main() {
	romPath := flag.String("rom", "", "Path to ROM file")
	checksumURL := flag.String("checksum", "", "URL to checksum file")
	flag.Parse()

	if *romPath == "" || *checksumURL == "" {
		fmt.Println("❌ Usage: rom-verification-engine -rom=<path> -checksum=<url>")
		os.Exit(1)
	}

	fmt.Println("🔐 ROM Verification Engine")
	fmt.Printf("📱 Verifying: %s\n", *romPath)

	result, err := verifyRom(*romPath, *checksumURL)
	if err != nil {
		fmt.Printf("❌ Error: %v\n", err)
		os.Exit(1)
	}

	if result.Valid {
		fmt.Println("✅ ROM verified — checksum matches")
		fmt.Printf("   Hash: %s\n", result.LocalSum)
	} else {
		fmt.Println("❌ CHECKSUM MISMATCH — ROM may be corrupted or tampered")
		fmt.Printf("   Local:  %s\n", result.LocalSum)
		fmt.Printf("   Remote: %s\n", result.RemoteSum)
		os.Exit(1)
	}
}
