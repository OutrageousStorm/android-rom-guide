package main

import (
	"archive/zip"
	"bufio"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

type ROMInfo struct {
	Device           string
	BuildID          string
	Flavor           string
	SecurityPatch    string
	ReleaseVersion   string
	Fingerprint      string
	AndroidVersion   string
	BuildTimestamp   string
	FileCount        int
	ApproximateSize  int64
}

func parseROMProperties(zipFile string) (*ROMInfo, error) {
	r, err := zip.OpenReader(zipFile)
	if err != nil {
		return nil, fmt.Errorf("failed to open ROM: %w", err)
	}
	defer r.Close()

	rom := &ROMInfo{}
	totalSize := int64(0)
	fileCount := 0

	// Try multiple paths for build.prop (different ROM structures)
	var buildPropFile *zip.File
	for _, file := range r.File {
		totalSize += int64(file.UncompressedSize)
		fileCount++

		if file.Name == "system/build.prop" || file.Name == "system/system/build.prop" {
			buildPropFile = file
			break
		}
	}

	if buildPropFile == nil {
		return rom, fmt.Errorf("build.prop not found in ROM")
	}

	rc, err := buildPropFile.Open()
	if err != nil {
		return nil, err
	}
	defer rc.Close()

	scanner := bufio.NewScanner(rc)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "#") {
			continue
		}

		parts := strings.SplitN(line, "=", 2)
		if len(parts) != 2 {
			continue
		}

		key, value := strings.TrimSpace(parts[0]), strings.TrimSpace(parts[1])

		switch key {
		case "ro.product.device":
			rom.Device = value
		case "ro.build.id":
			rom.BuildID = value
		case "ro.build.flavor":
			rom.Flavor = value
		case "ro.build.version.security_patch":
			rom.SecurityPatch = value
		case "ro.build.version.release":
			rom.ReleaseVersion = value
		case "ro.build.fingerprint":
			rom.Fingerprint = value
		case "ro.build.version.base_os":
			rom.AndroidVersion = value
		case "ro.build.date.utc":
			rom.BuildTimestamp = value
		}
	}

	rom.FileCount = fileCount
	rom.ApproximateSize = totalSize

	return rom, nil
}

func compareROMs(rom1, rom2 *ROMInfo) {
	fmt.Println("\n=== ROM Comparison ===\n")
	fmt.Printf("%-25s | %-30s | %-30s\n", "Property", rom1.Device, rom2.Device)
	fmt.Println(strings.Repeat("-", 90))

	// Device
	cmp := "✓"
	if rom1.Device != rom2.Device {
		cmp = "✗ DIFFERENT"
	}
	fmt.Printf("%-25s | %-30s | %-30s [%s]\n", "Device", rom1.Device, rom2.Device, cmp)

	// Build ID
	cmp = "✓"
	if rom1.BuildID != rom2.BuildID {
		cmp = "✗ DIFFERENT"
	}
	fmt.Printf("%-25s | %-30s | %-30s [%s]\n", "Build ID", rom1.BuildID, rom2.BuildID, cmp)

	// Flavor
	cmp = "✓"
	if rom1.Flavor != rom2.Flavor {
		cmp = "✗ DIFFERENT"
	}
	fmt.Printf("%-25s | %-30s | %-30s [%s]\n", "Flavor", rom1.Flavor, rom2.Flavor, cmp)

	// Security Patch
	cmp = "✓"
	if rom1.SecurityPatch != rom2.SecurityPatch {
		cmp = "⚠ DIFFERENT"
	}
	fmt.Printf("%-25s | %-30s | %-30s [%s]\n", "Security Patch", rom1.SecurityPatch, rom2.SecurityPatch, cmp)

	// Release Version
	cmp = "✓"
	if rom1.ReleaseVersion != rom2.ReleaseVersion {
		cmp = "✗ DIFFERENT"
	}
	fmt.Printf("%-25s | %-30s | %-30s [%s]\n", "Release", rom1.ReleaseVersion, rom2.ReleaseVersion, cmp)

	// File Count
	fmt.Printf("%-25s | %-30d | %-30d\n", "Files", rom1.FileCount, rom2.FileCount)

	// Size
	fmt.Printf("%-25s | %-30s | %-30s\n",
		"Approximate Size",
		formatSize(rom1.ApproximateSize),
		formatSize(rom2.ApproximateSize),
	)

	fmt.Println()
}

func formatSize(bytes int64) string {
	sizes := []string{"B", "KB", "MB", "GB"}
	size := float64(bytes)
	i := 0

	for size >= 1024 && i < len(sizes)-1 {
		size /= 1024
		i++
	}

	return fmt.Sprintf("%.2f %s", size, sizes[i])
}

func printROMInfo(rom *ROMInfo, filename string) {
	fmt.Printf("\n=== %s ===\n\n", filename)
	fmt.Printf("Device:          %s\n", rom.Device)
	fmt.Printf("Build ID:        %s\n", rom.BuildID)
	fmt.Printf("Flavor:          %s\n", rom.Flavor)
	fmt.Printf("Release:         %s\n", rom.ReleaseVersion)
	fmt.Printf("Security Patch:  %s\n", rom.SecurityPatch)
	fmt.Printf("Fingerprint:     %s\n", rom.Fingerprint)
	fmt.Printf("Files:           %d\n", rom.FileCount)
	fmt.Printf("Approx Size:     %s\n", formatSize(rom.ApproximateSize))
	fmt.Println()
}

func main() {
	flag.Parse()
	args := flag.Args()

	if len(args) == 0 {
		fmt.Println("Usage: rom-analyzer <rom1.zip> [rom2.zip]")
		fmt.Println("\nAnalyzes Android ROM files and optionally compares two ROMs")
		os.Exit(1)
	}

	rom1, err := parseROMProperties(args[0])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing ROM 1: %v\n", err)
		os.Exit(1)
	}

	printROMInfo(rom1, filepath.Base(args[0]))

	if len(args) > 1 {
		rom2, err := parseROMProperties(args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error parsing ROM 2: %v\n", err)
			os.Exit(1)
		}

		printROMInfo(rom2, filepath.Base(args[1]))
		compareROMs(rom1, rom2)
	}
}
