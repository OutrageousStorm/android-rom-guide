# Safe ADB Sideload

Sideload ROMs with checksums, rollback safety, and error recovery.

## Pre-sideload checklist

```bash
# 1. Verify ROM signature
sha256sum rom.zip > rom.sha256
# Compare with official source

# 2. Backup current state
adb reboot recovery
# In TWRP: Backup → System + Vendor + Data

# 3. Check space
adb shell df /data /system /vendor
# Need at least ROM size × 1.5 free space
```

## Safe sideload process

```bash
# Boot to recovery
adb reboot recovery

# In TWRP shell:
twrp sideload rom.zip

# Monitor on PC:
adb sideload rom.zip 2>&1 | tee sideload.log
```

## Rollback if it goes wrong

```bash
# Boot back to recovery
adb reboot bootloader
fastboot boot TWRP.img

# In TWRP:
Restore → pick backup → Restore All Partitions

# Verify
adb shell getprop ro.build.fingerprint
```

## Network timeout fixes

If sideload stalls:

```bash
adb reconnect
# In recovery: Advanced → Sideload again
```
