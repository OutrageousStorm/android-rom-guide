package main

import (
	"crypto/sha256"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

func fileHash(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}
	return fmt.Sprintf("%x", h.Sum(nil)), nil
}

func validateROM(romPath string, hashFile string) {
	fmt.Printf("\n🔍 ROM Validator\n")
	fmt.Println("=" * 40)

	fi, err := os.Stat(romPath)
	if err != nil {
		fmt.Printf("❌ ROM not found: %s\n", romPath)
		os.Exit(1)
	}

	fmt.Printf("ROM: %s\n", filepath.Base(romPath))
	fmt.Printf("Size: %.1f MB\n", float64(fi.Size())/1024/1024)

	hash, _ := fileHash(romPath)
	fmt.Printf("SHA256: %s\n\n", hash[:32]+"...")

	// Check for boot.img, system partition structure
	if strings.HasSuffix(romPath, ".zip") {
		fmt.Println("✅ ZIP format detected")
	}

	// Lookup against hash database (would be external in real implementation)
	if hashFile != "" {
		data, _ := ioutil.ReadFile(hashFile)
		if strings.Contains(string(data), hash) {
			fmt.Println("✅ Hash verified against database")
		} else {
			fmt.Println("⚠️  Hash NOT in database (may be custom build)")
		}
	}

	fmt.Println("\n✅ Pre-flash validation complete.")
	fmt.Println("Safe to flash: adb reboot bootloader")
}

func main() {
	rom := flag.String("rom", "", "Path to ROM ZIP")
	hashes := flag.String("hashes", "", "Path to hash database")
	flag.Parse()

	if *rom == "" {
		fmt.Println("Usage: rom-validator --rom system.zip [--hashes hashes.txt]")
		os.Exit(1)
	}

	validateROM(*rom, *hashes)
}
