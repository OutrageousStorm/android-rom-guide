# ROM Flashing Errors & Solutions

## "Device not found" in fastboot

```bash
# Check device list
fastboot devices

# If empty:
adb reboot bootloader
adb reboot fastboot
# (not both — depends on your device)

# Restart adb daemon
adb kill-server
adb devices
```

## "Remote: Failed to parse bootloader message"

Your bootloader is locked or doesn't support the ROM. 

```bash
# Check lock status
fastboot oem device-info
# or
fastboot getvar locked

# Unlock (wipes data)
fastboot oem unlock
# or
fastboot flashing unlock
```

## "cannot load 'source.prop'" during sideload

Recovery can't read the ROM file.

```bash
# Ensure ROM is on device
adb push rom.zip /sdcard/

# In recovery:
# Choose "Apply update from ADB"
adb sideload rom.zip
```

## "Flashing is not allowed for Critical partitions"

The ROM includes system/vendor patches but bootloader won't allow it.

```bash
# Flash individual partitions:
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash product product.img
# Don't use `-w` (that erases them)
```

## Stuck in bootloop after flash

```bash
# 1. Try wiping data (factory reset)
adb reboot recovery
# Menu → Wipe → Factory reset

# 2. If that fails, use fastboot to restore:
fastboot -w
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot reboot

# 3. Last resort: reflash original ROM
```

## "Signature verification failed"

ROM file is corrupted or incomplete.

```bash
# Re-download ROM — check file size/MD5
md5sum rom.zip
# Compare against official release notes

# Verify on device before flashing:
adb push rom.zip /sdcard/
adb shell md5sum /sdcard/rom.zip
```
