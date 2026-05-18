# Bootloop Recovery Guide

Device stuck in bootloop? Here's how to recover.

## Diagnose bootloop type

```bash
# Monitor logs during boot
adb logcat -b all | grep -E "(FATAL|ERROR|CRASH|ANR)"

# Check system.img integrity
adb shell dumpsys meminfo | grep "Total RAM"
adb shell dmesg | tail -50
```

### Types of bootloops

1. **Infinite boot animation** — system starting, hangs before home screen
2. **System crash bootloop** — SystemUI crashes repeatedly
3. **Kernel panic** — device reboots every 30 seconds (dmesg shows panic)
4. **Recovery loop** — stuck booting to recovery

## Recovery steps

### Step 1: Boot to recovery
```bash
adb reboot recovery
# If adb doesn't work, use hardware buttons:
# Power + Volume Down (most devices)
```

### Step 2: Check filesystem
```bash
# From recovery ADB
adb shell fsck.ext4 -n /dev/block/mmcblk0p30  # system partition
adb shell e2fsck -n /dev/block/mmcblk0pXX      # userdata
```

### Step 3: Wipe cache
```bash
adb shell rm -rf /cache/*
adb shell rm -rf /data/cache/*
```

### Step 4: Restore from backup
```bash
# If you have a TWRP backup
adb push backup.tar /sdcard/
# Restore via TWRP UI or:
adb shell tar -xf /sdcard/backup.tar -C /
```

### Step 5: Flash previous ROM
```bash
# If current ROM is corrupted, flash a known-good build
adb reboot bootloader
fastboot flash system system.img
fastboot flash boot boot.img
fastboot reboot
```

### Step 6: Factory reset (last resort)
```bash
adb reboot recovery
# Via TWRP: Wipe → Data, Cache, Dalvik
# Via Stock Recovery: Factory reset (loses all data)
```

## Prevent bootloops

1. **Always test ROM before flashing system** — use GSI first
2. **Keep working backup** — TWRP backups saved offline
3. **Avoid mix-and-match** — don't flash vendor.img from different ROM
4. **Monitor logs** — `adb logcat` before rebooting
5. **Slow rollback** — downgrade gradually (never skip major versions)

## If nothing works

1. Download factory image for your device
2. Flash via fastboot from computer
3. Device returns to stock (data may be wiped)

Resources:
- [Fastboot tutorial](https://www.xda-developers.com/how-to-install-adb/)
- [TWRP recovery](https://twrp.me/)
- Stock images: Google Factory Images, Samsung Firmware, OnePlus firmware
