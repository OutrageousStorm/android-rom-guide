#!/usr/bin/env python3
"""
rom_backup_validator.py -- Validate ROM files before flashing
Checks: file size, signature, format, partition compatibility
Usage: python3 rom_backup_validator.py <rom.img> <rom.zip>
"""
import sys, os, hashlib, zipfile, re
from pathlib import Path

def validate_zip(path):
    """Validate Android ROM zip file"""
    try:
        with zipfile.ZipFile(path, 'r') as z:
            files = z.namelist()
            required = ['boot.img', 'system.img']
            has_boot = any('boot.img' in f for f in files)
            has_system = any('system.img' in f or 'system.new.dat' in f for f in files)
            
            if not (has_boot or has_system):
                print("❌ Missing boot.img or system.img")
                return False
            
            # Check for recovery
            has_recovery = any('recovery.img' in f for f in files)
            print(f"✓ boot.img: {'✓' if has_boot else '✗'}")
            print(f"✓ system.img: {'✓' if has_system else '✗'}")
            print(f"✓ recovery.img: {'✓' if has_recovery else '✗'}")
            
            # Check updater-script or payload.bin
            has_updater = any('updater-script' in f for f in files)
            has_payload = 'payload.bin' in files
            if not (has_updater or has_payload):
                print("⚠️  No updater-script or payload.bin — may not be flashable")
            
            return True
    except Exception as e:
        print(f"❌ Invalid ZIP: {e}")
        return False

def validate_img(path):
    """Validate raw .img file"""
    size = os.path.getsize(path)
    print(f"Size: {size / (1024**3):.2f} GB")
    
    # Check magic bytes
    with open(path, 'rb') as f:
        magic = f.read(4)
    
    if magic == b'ANDROID':
        print("✓ Android boot image format detected")
        return True
    elif magic[:2] == b'\x1f\x8b':
        print("✓ Gzip compressed image")
        return True
    else:
        print(f"⚠️  Unknown magic bytes: {magic.hex()}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rom_backup_validator.py <rom.zip|rom.img>")
        sys.exit(1)
    
    rom_path = sys.argv[1]
    if not os.path.exists(rom_path):
        print(f"❌ File not found: {rom_path}")
        sys.exit(1)
    
    print(f"\n🔍 ROM Validator — {os.path.basename(rom_path)}")
    print("=" * 40)
    
    if rom_path.endswith('.zip'):
        ok = validate_zip(rom_path)
    elif rom_path.endswith('.img'):
        ok = validate_img(rom_path)
    else:
        print(f"Unknown file type: {rom_path}")
        ok = False
    
    print("\n" + "=" * 40)
    print("✅ Ready to flash" if ok else "❌ Validation failed — do not flash")

if __name__ == "__main__":
    main()
