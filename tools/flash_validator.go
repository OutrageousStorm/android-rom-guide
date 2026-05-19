package main

import (
	"bufio"
	"crypto/sha256"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

// ValidateROMFile checks ROM integrity before flashing
// Usage: flash_validator rom.zip
func main() {
	flag.Parse()
	if flag.NArg() == 0 {
		fmt.Println("Usage: flash_validator <rom.zip>")
		os.Exit(1)
	}

	romFile := flag.Arg(0)
	file, err := os.Open(romFile)
	if err != nil {
		fmt.Printf("❌ Cannot open ROM: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	fileInfo, _ := file.Stat()
	size := fileInfo.Size()
	fmt.Printf("📦 ROM: %s (%d MB)\n", filepath.Base(romFile), size/1024/1024)

	// Calculate SHA256
	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		fmt.Printf("❌ Hash error: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("✓ SHA256: %x\n", hash.Sum(nil))

	// Check file structure (minimal ZIP validation)
	file.Seek(0, 0)
	header := make([]byte, 4)
	file.Read(header)
	if header[0] == 0x50 && header[1] == 0x4B { // ZIP magic
		fmt.Println("✓ Valid ZIP archive")
	} else {
		fmt.Println("❌ Not a valid ZIP file")
		os.Exit(1)
	}

	fmt.Println("✅ ROM ready to flash")
}
