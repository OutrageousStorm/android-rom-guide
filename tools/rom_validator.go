package main

import (
	"fmt"
	"os"
	"path/filepath"
	"io/ioutil"
	"crypto/sha256"
	"encoding/hex"
)

// ValidateROM checks ROM file integrity before flashing
func ValidateROM(romPath string) (bool, error) {
	info, err := os.Stat(romPath)
	if err != nil {
		return false, fmt.Errorf("ROM file not found: %v", err)
	}

	// Check minimum file size (most ROMs 500MB+)
	minSize := int64(500 * 1024 * 1024)
	if info.Size() < minSize {
		return false, fmt.Errorf("ROM too small (%d bytes, expected ≥ %d)", info.Size(), minSize)
	}

	// Verify ZIP structure
	data, _ := ioutil.ReadFile(romPath)
	if len(data) < 4 || string(data[:2]) != "PK" {
		return false, fmt.Errorf("Not a valid ZIP file (invalid magic bytes)")
	}

	return true, nil
}

// CheckSHA256 verifies ROM checksum against published hash
func CheckSHA256(romPath, expectedHash string) (bool, error) {
	data, err := ioutil.ReadFile(romPath)
	if err != nil {
		return false, err
	}
	hash := sha256.Sum256(data)
	actual := hex.EncodeToString(hash[:])
	return actual == expectedHash, nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: rom_validator <rom_file> [sha256]")
		os.Exit(1)
	}

	romPath := os.Args[1]
	ok, err := ValidateROM(romPath)
	if err != nil {
		fmt.Printf("❌ Validation failed: %v\n", err)
		os.Exit(1)
	}

	if ok {
		fmt.Printf("✓ ROM file valid (%s)\n", romPath)
		if len(os.Args) > 2 {
			expected := os.Args[2]
			match, _ := CheckSHA256(romPath, expected)
			if match {
				fmt.Println("✓ SHA256 checksum matches")
			} else {
				fmt.Println("❌ SHA256 mismatch")
			}
		}
	}
}
