# A/B Partition Scheme Guide

Modern Android uses A/B (seamless) partitions for safer OTA updates.

## How it works

```
Traditional (A-only):
  /boot → kernel
  /system → OS
  /data → user data
  
A/B scheme:
  /boot_a, /boot_b → two kernel slots
  /system_a, /system_b → two OS slots
  /data → shared (one copy)
```

When an OTA arrives:
1. Download update to inactive slot
2. Verify signature on inactive slot
3. Set inactive as "next boot"
4. Reboot — boots inactive (now active)
5. If boot fails, automatically rollback to old slot

## Checking your device

```bash
adb shell getprop ro.boot.slot_suffix
# Output: _a or _b = you're on an A/B device
# Empty = A-only device
```

## Flashing to A/B devices

```bash
# Flash to current slot
fastboot flash boot boot.img

# Or specify slot explicitly
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img

# Check current slot
fastboot getvar current-slot

# Switch to other slot (for testing)
fastboot set_active other
```

## Recovery on A/B devices

- Some A/B devices use **recovery-as-boot** — recovery is a ramdisk appended to boot
- Others have dedicated recovery slots
- TWRP on A/B: install to current slot, reboot to recovery via `adb reboot recovery`

## OTA package differences

A/B OTA packages (block-based or payload-based) are incompatible with A-only recovery ROMs. Always check device compatibility before flashing an OTA.
