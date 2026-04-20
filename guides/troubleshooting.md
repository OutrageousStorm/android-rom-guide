# ROM Flashing Troubleshooting

## Boot Loop After Flash

### Diagnosis
- Device stuck on splash screen or bootloader logo
- Continuous restarts every 5-10 seconds
- No recovery access possible

### Common causes & fixes

**1. Vendor/Firmware mismatch**
```bash
# You flashed a ROM for different device or build variant
# Solution: get correct ROM for your exact device codename + region
adb reboot bootloader
fastboot flash recovery twrp.img
fastboot reboot recovery
# In recovery: restore backup or re-flash correct ROM
```

**2. Corrupted GApps package**
```bash
# GApps too old or wrong Android version
# Solution: wipe System, reflash ROM, use NEW GApps
# In TWRP:
#   Wipe → Advanced → System
#   Install → ROM → (no GApps this time)
#   Reboot → setup without GApps first
#   If stable: go back to recovery, install newer GApps
```

**3. Incompatible Magisk version**
```bash
# Magisk built for different API level
# Solution: boot into recovery, uninstall Magisk
# adb sideload magisk_latest.apk
```

**4. Full data wipe didn't work**
```bash
# Old data conflicts with new ROM
# Solution: wipe Data + Cache + Dalvik
# In TWRP: Wipe → Advanced Wipe → check all three
```

## Stuck in Recovery

**Can't boot to system even from recovery**

```bash
# Try ADB sideload
adb sideload rom.zip

# If that fails, try re-flashing kernel/boot
adb reboot bootloader
fastboot flash boot boot.img
fastboot reboot
```

## "E: can't find recovery" (TWRP message)

Means recovery partition is corrupted:
```bash
# Reflash TWRP
fastboot flash recovery twrp.img
fastboot boot twrp.img  # temp boot to verify
```

## Stuck on "Android is starting..."

**Kernel panic or corruption**

```bash
# Force reboot by holding power 10 seconds
# Get to recovery, reinstall ROM
# If using custom kernel, switch to stock kernel first
```

## Device won't recognize USB

```bash
adb devices  # shows nothing

# Try:
1. Different USB cable
2. Different port
3. Disable USB authentication: adb kill-server && adb devices
4. Enable "ADB debugging" on device (if bootable)
   Settings → Developer → USB debugging

# If stuck in bootloader:
fastboot devices  # should show serial
```

## Bricked (won't boot, no recovery, no fastboot)

**Last resort:**

1. **NAND rework** (professional, expensive)
2. **Unbrick tools** (OEM-specific, check XDA)
3. **EDL mode** (Qualcomm devices) — may be recoverable

For Qualcomm:
```bash
# Hold Vol Down + Power for 10+ seconds
# Should show "Qualcomm HS-USB QDLoader 9008" in Device Manager (Windows)
adb devices  # if in EDL shows as COM port
# Use Qualcomm Emergency Download Mode tool + stock firmware
```

## Still stuck?

Check XDA Developers for your specific device:
- https://forum.xda-developers.com
- Search: "[device] ROM/kernel troubleshooting"
- Post on XDA — experts will help
