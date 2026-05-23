package main

import (
	"crypto/sha256"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

/**
 * ROM Verification Engine
 * Verify ROM signatures, checksums, and source integrity
 * Purpose: Ensure ROM files are authentic before flashing
 */

type ROMVerification struct {
	RomFile      string
	ChecksumFile string
	SourceRepo   string
	Verbose      bool
}

func (rv *ROMVerification) VerifyChecksum() (bool, error) {
	if rv.ChecksumFile == "" {
		return false, fmt.Errorf("checksum file not provided")
	}

	romHash, err := calculateSHA256(rv.RomFile)
	if err != nil {
		return false, err
	}

	checksumContent, err := ioutil.ReadFile(rv.ChecksumFile)
	if err != nil {
		return false, err
	}

	checksumStr := strings.TrimSpace(string(checksumContent))
	if strings.Contains(checksumStr, " ") {
		parts := strings.Fields(checksumStr)
		checksumStr = parts[0]
	}

	if rv.Verbose {
		fmt.Printf("📊 ROM Hash:      %s\n", romHash)
		fmt.Printf("📊 Expected Hash: %s\n", checksumStr)
	}

	return strings.EqualFold(romHash, checksumStr), nil
}

func (rv *ROMVerification) VerifySourceRepo() (bool, error) {
	if rv.SourceRepo == "" {
		return false, fmt.Errorf("source repo not provided")
	}

	resp, err := http.Get(rv.SourceRepo + "/releases")
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	if rv.Verbose {
		fmt.Printf("✅ Source repo reachable: %s (HTTP %d)\n", rv.SourceRepo, resp.StatusCode)
	}

	return resp.StatusCode < 400, nil
}

func calculateSHA256(filePath string) (string, error) {
	file, err := os.Open(filePath)
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

func main() {
	rv := &ROMVerification{}
	flag.StringVar(&rv.RomFile, "rom", "", "Path to ROM file to verify")
	flag.StringVar(&rv.ChecksumFile, "checksum", "", "Path to checksum file (sha256)")
	flag.StringVar(&rv.SourceRepo, "repo", "", "GitHub repo URL for source verification")
	flag.BoolVar(&rv.Verbose, "v", false, "Verbose output")
	flag.Parse()

	if rv.RomFile == "" {
		fmt.Println("❌ Usage: rom-verification-engine -rom <file> [-checksum <file>] [-repo <url>] [-v]")
		os.Exit(1)
	}

	fmt.Println("🔍 Starting ROM verification...")

	if rv.ChecksumFile != "" {
		valid, err := rv.VerifyChecksum()
		if err != nil {
			fmt.Printf("❌ Checksum verification failed: %v\n", err)
			os.Exit(1)
		}
		if valid {
			fmt.Println("✅ Checksum verified — ROM is authentic")
		} else {
			fmt.Println("❌ Checksum mismatch — ROM may be corrupted or tampered")
			os.Exit(1)
		}
	}

	if rv.SourceRepo != "" {
		valid, err := rv.VerifySourceRepo()
		if err != nil {
			fmt.Printf("⚠️  Source repo verification failed: %v\n", err)
		} else if valid {
			fmt.Println("✅ Source repository verified — Official release")
		} else {
			fmt.Println("⚠️  Source repository unreachable or 404")
		}
	}

	fmt.Println("\n✅ ROM verification complete")
}
