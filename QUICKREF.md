# ROM Flashing Quick Reference

## Before You Flash
```bash
# Unlock bootloader (device-specific, wipes data)
adb reboot bootloader
fastboot oem unlock
# OR
fastboot flashing unlock

# Verify bootloader is unlocked
fastboot getvar unlock-state
# Expected: "unlocked"
```

## Flash ROM via TWRP
```bash
# Boot to TWRP recovery
adb reboot recovery

# In TWRP:
# Wipe → Advanced Wipe → select: Dalvik/ART, System, Data, Cache
# Install → select ROM.zip → swipe to confirm
# (Optional) Install GApps.zip before first boot
# Reboot System
```

## Flash ROM via fastboot (A/B devices)
```bash
adb reboot bootloader

fastboot --set-active=other    # switch to inactive slot
fastboot -w                     # wipe userdata
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash boot boot.img
fastboot --set-active=a         # switch back to main slot
fastboot reboot
```

## Recovery from Bootloop
```bash
# Method 1: Re-flash the ROM
adb sideload rom.zip          # from recovery, use adb sideload

# Method 2: Restore backup
adb reboot recovery
# In TWRP: Restore → select your backup → swipe

# Method 3: Format everything and reflash
fastboot -w
fastboot flash system system.img
fastboot reboot
```

## ADB Sideload (cleanest install)
```bash
# From TWRP: Advanced → ADB Sideload
adb sideload rom.zip
adb sideload gapps.zip        # optional
adb sideload magisk.zip       # optional
# Device automatically reboots
```

## Common Partition Names (by device)
| Device | Boot | System | Vendor | Recovery |
|--------|------|--------|--------|----------|
| Pixel 4-5 | boot | system | vendor | — (recovery as boot) |
| Samsung S10+ | boot | system | vendor | recovery |
| OnePlus 8T | boot_a/boot_b | system_a/system_b | vendor_a/vendor_b | — |
| Xiaomi Mi 11 | boot | system | vendor | — |

## Magisk Install (post-ROM)
```bash
# Option A: Flash via recovery
adb sideload Magisk-vXX.zip

# Option B: Patch boot.img on PC
# 1. Extract boot.img from ROM zip
# 2. Push to device: adb push boot.img /sdcard/
# 3. In Magisk app: Install → Patch a File → boot.img
# 4. adb pull /sdcard/Download/magisk_patched_*.img
# 5. fastboot flash boot magisk_patched_*.img
```

## Verify Installation
```bash
# Check ROM version
adb shell getprop ro.build.version.release

# Verify root (if Magisk)
adb shell su -c "whoami"  # should print "root"

# Check boot slot (A/B devices)
adb shell getprop ro.boot.slot_suffix  # _a or _b
```

## Emergency ADB Mode
```bash
# If device won't boot past bootloader:
adb devices -l  # may still show as "bootloader"

# Sideload while in recovery:
adb sideload rom.zip    # requires TWRP/custom recovery
```
