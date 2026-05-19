#!/usr/bin/env python3
"""
rom-size-analyzer.py -- Analyze ROM zip file before flashing
Shows: partition sizes, system apps, bloatware candidates, free space after install
Usage: python3 rom-size-analyzer.py rom.zip
"""
import zipfile, sys, os, re
from collections import defaultdict

def analyze_rom(rom_path):
    if not os.path.exists(rom_path):
        print(f"File not found: {rom_path}"); sys.exit(1)

    print(f"\n📊 ROM Size Analyzer")
    print(f"File: {os.path.basename(rom_path)}")
    print("=" * 60)

    with zipfile.ZipFile(rom_path, 'r') as z:
        # Get system.img or system.new.dat
        files = z.namelist()
        total_size = sum(z.getinfo(f).file_size for f in files)
        print(f"\nTotal ZIP size: {total_size / 1024**3:.2f} GB")

        # Check image files
        for img in ['system.img', 'system.new.dat', 'vendor.img', 'boot.img', 'recovery.img']:
            if img in files:
                size = z.getinfo(img).file_size
                print(f"  {img:<20} {size / 1024**2:.0f} MB")

        # Check for bloatware patterns
        print(f"\nLikely bloatware (APKs > 50MB):")
        bloat = []
        for name in files:
            if name.endswith('.apk'):
                size = z.getinfo(name).file_size
                if size > 50 * 1024**2:
                    bloat.append((name, size))

        bloat.sort(key=lambda x: x[1], reverse=True)
        for apk, size in bloat[:10]:
            print(f"  {apk.split('/')[-1]:<35} {size / 1024**2:.1f} MB")

        # Check MD5 checksums
        if 'md5.txt' in files:
            print(f"\n✅ MD5 checksums present (flash validation available)")

        # Extract build info
        props_files = [f for f in files if 'build.prop' in f]
        print(f"\nBuild files: {len(props_files)}")
        for prop_file in props_files[:3]:
            print(f"  - {prop_file}")

        print(f"\n📝 Recommendation:")
        if total_size > 2 * 1024**3:
            print("  Large ROM (>2GB) — ensure sufficient free space on device")
        print("  Verify MD5 before flashing: adb devices should show connected device")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 rom-size-analyzer.py <rom.zip>")
        sys.exit(1)
    analyze_rom(sys.argv[1])
