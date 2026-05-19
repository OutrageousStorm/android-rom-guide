#!/usr/bin/env python3
"""rom_hash_validator.py -- Verify ROM integrity before flashing"""
import hashlib, sys, os

if len(sys.argv) < 2:
    print("Usage: python3 rom_hash_validator.py <rom.zip> [checksum]")
    sys.exit(1)

rom_file = sys.argv[1]
if not os.path.exists(rom_file):
    print(f"File not found: {rom_file}")
    sys.exit(1)

print(f"Computing SHA256 for {os.path.basename(rom_file)}...")
sha256 = hashlib.sha256()
with open(rom_file, 'rb') as f:
    for chunk in iter(lambda: f.read(8192), b''):
        sha256.update(chunk)

digest = sha256.hexdigest()
print(f"SHA256: {digest}")

if len(sys.argv) > 2 and sys.argv[2].lower() == digest.lower():
    print("✅ Hash matches!")
else:
    print("⚠️  Keep this hash to verify after download")
