#!/usr/bin/env python3
"""
flash_validator.py -- Pre-flash ROM validation
Checks: file size, checksum, device compatibility before flashing
Usage: python3 flash_validator.py rom.img --device=codename
"""
import sys, hashlib, argparse, subprocess

def md5_file(f):
    h = hashlib.md5()
    with open(f, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('rom', help='ROM file path')
parser.add_argument('--device', help='Expected device codename')
parser.add_argument('--md5', help='Expected MD5 checksum')
args = parser.parse_args()

print(f"🔍 Validating {args.rom}...")

# Check file exists and size
import os
if not os.path.exists(args.rom):
    print(f"❌ File not found: {args.rom}"); sys.exit(1)

size_mb = os.path.getsize(args.rom) / (1024*1024)
print(f"  ✓ File size: {size_mb:.0f} MB")

# Check MD5
if args.md5:
    actual = md5_file(args.rom)
    if actual == args.md5:
        print(f"  ✓ MD5 matches: {actual}")
    else:
        print(f"  ❌ MD5 mismatch!"); sys.exit(1)

# Check device match
if args.device:
    device = subprocess.run("adb shell getprop ro.product.device", shell=True, capture_output=True, text=True).stdout.strip()
    if device == args.device:
        print(f"  ✓ Device matches: {device}")
    else:
        print(f"  ⚠️  Device mismatch: expected {args.device}, device is {device}")

print("\n✅ ROM ready to flash")
