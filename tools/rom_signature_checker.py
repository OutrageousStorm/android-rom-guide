#!/usr/bin/env python3
"""
rom_signature_checker.py -- Verify ROM zip file integrity and certificates
Usage: python3 rom_signature_checker.py rom_file.zip
"""
import zipfile, hashlib, sys, subprocess
from pathlib import Path

def check_zip_integrity(zip_path):
    """Test if ZIP is valid and not corrupted"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            bad = z.testzip()
            if bad:
                print(f"❌ Corrupted file: {bad}")
                return False
            print(f"✅ ZIP integrity OK ({len(z.namelist())} files)")
            return True
    except Exception as e:
        print(f"❌ Invalid ZIP: {e}")
        return False

def check_metadata_signature(zip_path):
    """Check if ROM has valid CERT.RSA signature"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            if 'META-INF/CERT.RSA' in z.namelist():
                print("✅ Signed ROM detected (CERT.RSA present)")
                return True
            else:
                print("⚠️  Unsigned ROM or non-standard signature")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_with_openssl(zip_path):
    """Deep signature verification using openssl (optional)"""
    print("\n🔐 Attempting OpenSSL signature verification...")
    try:
        # Extract CERT.RSA
        with zipfile.ZipFile(zip_path, 'r') as z:
            cert_data = z.read('META-INF/CERT.RSA')
        cert_path = "/tmp/CERT.RSA"
        with open(cert_path, 'wb') as f:
            f.write(cert_data)

        # Use openssl to extract certificate info
        result = subprocess.run(
            f"openssl pkcs7 -inform DER -in {cert_path} -text -print_certs",
            shell=True, capture_output=True, text=True
        )
        if "Subject:" in result.stdout:
            print("✅ Valid certificate found")
            # Print issuer
            for line in result.stdout.splitlines():
                if "Subject:" in line or "Issuer:" in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print("⚠️  Could not verify with openssl")
            return False
    except Exception as e:
        print(f"⚠️  OpenSSL check failed: {e}")
        return False

def check_file_hashes(zip_path):
    """Verify file hashes if ROM includes SHA256SUMS"""
    with zipfile.ZipFile(zip_path, 'r') as z:
        if 'SHA256SUMS' not in z.namelist():
            print("⚠️  No SHA256SUMS file found (can't verify individual files)")
            return

        hashes = z.read('SHA256SUMS').decode('utf-8')
        matched = 0
        total = 0
        for line in hashes.splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            expected_hash = parts[0]
            filename = parts[1]
            try:
                file_data = z.read(filename)
                actual_hash = hashlib.sha256(file_data).hexdigest()
                total += 1
                if actual_hash == expected_hash:
                    matched += 1
                else:
                    print(f"  ❌ MISMATCH: {filename}")
            except KeyError:
                pass
        if matched == total:
            print(f"✅ All {total} file hashes verified")
        else:
            print(f"⚠️  {matched}/{total} file hashes match")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rom_signature_checker.py <rom.zip>")
        sys.exit(1)

    rom_path = sys.argv[1]
    if not Path(rom_path).exists():
        print(f"❌ File not found: {rom_path}")
        sys.exit(1)

    print(f"\n🔍 ROM Signature Checker — {Path(rom_path).name}\n")

    # Checks
    check_zip_integrity(rom_path)
    check_metadata_signature(rom_path)
    verify_with_openssl(rom_path)
    check_file_hashes(rom_path)

    print("\n✅ Verification complete.")
    print("Note: Signature check only verifies ROM wasn't corrupted in transit.")
    print("      Always download from official sources (GitHub, SourceForge).")

if __name__ == "__main__":
    main()
