package main

import (
	"bufio"
	"crypto/md5"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	romPath := flag.String("rom", "", "Path to ROM zip file")
	checksumPath := flag.String("checksum", "", "Path to checksum file (MD5SUMS)")
	flag.Parse()

	if *romPath == "" {
		fmt.Println("Usage: flash_validator -rom <path.zip> -checksum <MD5SUMS>")
		os.Exit(1)
	}

	// Verify ROM exists
	if _, err := os.Stat(*romPath); err != nil {
		fmt.Printf("❌ ROM not found: %s
", *romPath)
		os.Exit(1)
	}

	fmt.Println("
🔍 ROM Validator")
	fmt.Println("================")

	// Calculate MD5
	f, err := os.Open(*romPath)
	if err != nil {
		fmt.Printf("❌ Cannot open ROM: %v
", err)
		os.Exit(1)
	}
	defer f.Close()

	h := md5.New()
	if _, err := io.Copy(h, f); err != nil {
		fmt.Printf("❌ Read error: %v
", err)
		os.Exit(1)
	}
	calculated := fmt.Sprintf("%x", h.Sum(nil))
	fmt.Printf("  Calculated: %s
", calculated)

	// Check against file if provided
	if *checksumPath != "" {
		file, err := os.Open(*checksumPath)
		if err != nil {
			fmt.Printf("⚠️  Checksum file not found: %s
", *checksumPath)
		} else {
			defer file.Close()
			scanner := bufio.NewScanner(file)
			for scanner.Scan() {
				line := scanner.Text()
				parts := strings.Fields(line)
				if len(parts) >= 2 {
					expected := parts[0]
					filename := parts[1]
					romName := filepath.Base(*romPath)
					if strings.Contains(filename, romName) {
						fmt.Printf("  Expected:   %s
", expected)
						if expected == calculated {
							fmt.Println("  ✅ Checksum valid!")
						} else {
							fmt.Println("  ❌ Checksum mismatch! File may be corrupted.")
							os.Exit(1)
						}
						return
					}
				}
			}
		}
	}

	fmt.Println("\n✅ ROM ready to flash!")
}
