package main

import (
	"crypto/sha256"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

// ValidateROMFile checks ROM integrity before flashing
// Usage: ./rom_flash_validator -rom stock.img -sha256 abc123def456...
// or:    ./rom_flash_validator -rom stock.img -checksum stock.img.sha256
func main() {
	romPath := flag.String("rom", "", "Path to ROM/boot/recovery image")
	sha256Hash := flag.String("sha256", "", "Expected SHA256 hash")
	checksumFile := flag.String("checksum", "", "Path to .sha256 or .md5 checksum file")
	flag.Parse()

	if *romPath == "" {
		fmt.Println("Usage: rom_flash_validator -rom <file> [-sha256 <hash> | -checksum <file>]")
		os.Exit(1)
	}

	data, err := ioutil.ReadFile(*romPath)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		os.Exit(1)
	}

	actual := fmt.Sprintf("%x", sha256.Sum256(data))
	fmt.Printf("File: %s\n", filepath.Base(*romPath))
	fmt.Printf("Size: %.2f MB\n", float64(len(data))/1024/1024)
	fmt.Printf("SHA256: %s\n\n", actual)

	if *sha256Hash != "" {
		*sha256Hash = strings.ToLower(*sha256Hash)
		if *sha256Hash == actual {
			fmt.Println("✅ HASH VERIFIED - Safe to flash")
			os.Exit(0)
		} else {
			fmt.Printf("❌ HASH MISMATCH\n  Expected: %s\n  Got:      %s\n", *sha256Hash, actual)
			os.Exit(1)
		}
	}

	if *checksumFile != "" {
		content, err := ioutil.ReadFile(*checksumFile)
		if err != nil {
			fmt.Printf("Error reading checksum file: %v\n", err)
			os.Exit(1)
		}
		checksum := strings.Fields(string(content))[0]
		if strings.ToLower(checksum) == actual {
			fmt.Println("✅ CHECKSUM VERIFIED - Safe to flash")
			os.Exit(0)
		} else {
			fmt.Printf("❌ CHECKSUM MISMATCH\n  Expected: %s\n  Got:      %s\n", checksum, actual)
			os.Exit(1)
		}
	}

	fmt.Println("⚠️  No hash provided for verification (use -sha256 or -checksum)")
}
