# GrapheneOS Advanced Security Hardening

Maximize privacy and security on GrapheneOS with kernel and system hardening.

## Kernel Protections (Built-in)
GrapheneOS kernel includes:
- **CFI** — Control Flow Integrity prevents ROP attacks
- **ShadowCallStack** — protects return address integrity
- **MTE** — Memory Tagging Extension catches memory bugs
- **SMAC** — mandatory access control for processes

Verify kernel hardening:
```bash
adb shell cat /proc/config.gz | gunzip | grep "CONFIG_CFI\|CONFIG_SHADOW\|CONFIG_MTE"
```

## Secure Enclave (Hardware)
GrapheneOS uses Secure Enclave for:
- Keystore operations (AES encryption/decryption)
- Biometric verification (fingerprint/face)
- Attestation challenges (prove device identity)

Check Secure Enclave status:
```bash
adb shell getprop ro.hardware.keystore
adb shell cmd keystore_cli list
adb shell cmd keystore_cli attest
```

## Network Hardening
```bash
# Force DNS-over-HTTPS via Orbot
adb shell settings put global http_proxy "127.0.0.1:8118"

# Monitor all DNS queries
adb shell dumpsys netd | grep -i "dns"

# Disable cleartext traffic (HTTPS only)
adb shell settings put global http_proxy_exclude_all 1
```

## File Encryption
GrapheneOS uses strong encryption:
- **Metadata encryption** — encrypts filenames, sizes, permissions
- **Per-file keys** — each file has unique encryption key
- **Scrypt KDF** — slow key derivation resists brute force

Check encryption:
```bash
adb shell dumpsys diskstats | grep -i encrypt
adb shell getprop ro.crypto.state
adb shell getprop ro.crypto.type
```

## Attestation & Verification
Verify device hasn't been modified:
```bash
# Check bootloader state
adb shell getprop ro.boot.verifiedbootstate

# Check SELinux mode
adb shell getenforce

# Verify system partitions
adb shell dm verity_status
```
