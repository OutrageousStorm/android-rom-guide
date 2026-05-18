# Complete TWRP Flashing Guide

Step-by-step guide to flash ROMs via TWRP recovery on any device.

## Prerequisites

1. **TWRP installed** — device boots to TWRP recovery
2. **ROM ZIP file** — downloaded and validated (MD5/SHA256 checksum)
3. **GApps (optional)** — if the ROM is AOSP-based and you want Google apps
4. **Magisk (optional)** — if you want root after flashing

## Flashing process

### 1. Boot to recovery
```bash
adb reboot recovery
# Or press: Power + Volume Down (keep held)
```

### 2. Backup current ROM (inside TWRP)
- **Backup** → Select `/data`, `/system`, `/boot`
- Confirm → backup creates timestamped folder in `/TWRP/BACKUPS`

### 3. Wipe for clean install
- **Wipe** → **Advanced Wipe**
- Select: `/system`, `/data`, `/cache`, `/dalvik-cache`
- Swipe to confirm
- **DO NOT** wipe `/sdcard` or you'll lose the ROM file

### 4. Flash ROM
- **Install** → navigate to ROM ZIP
- Swipe to confirm
- Wait 1-5 minutes depending on ROM size

### 5. Flash GApps (if desired)
- **Install** → GApps ZIP
- Swipe to confirm

### 6. Flash Magisk (if desired for root)
- **Install** → Magisk ZIP
- Swipe to confirm

### 7. Reboot
- **Reboot** → **System**
- Wait 5-10 minutes for first boot (longer is normal)

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "Installation aborted" | ROM incompatible with device | Verify ROM for correct device model |
| Bootloop | Missing dependencies (vendor, libs) | Flash vendor image separately |
| No system partition | Wrong TWRP build | Reinstall correct TWRP version |
| Can't wipe /data | Encryption | Format /data (destructive) in Advanced Wipe options |
| Magisk won't install after ROM | ROM has signature check | Disable signature verification in TWRP settings |

## Safe flashing checklist

✅ Device is charged to 100%
✅ ROM file matches device model exactly
✅ MD5/SHA256 matches (if provided)
✅ Backup created before wiping
✅ Install order: ROM → GApps → Magisk (not the reverse)
✅ Don't interrupt during flash (no unplugging!)
✅ First boot takes 5-15 minutes — be patient

## Recovery commands (without TWRP GUI)

```bash
# Sideload ROM (if TWRP won't boot)
adb sideload rom.zip

# Flash via fastbootd
fastboot flash system system.img
fastboot flash boot boot.img
fastboot flash vendor vendor.img
fastboot reboot

# List TWRP backups
adb shell ls /TWRP/BACKUPS/*/
```

---

**Related guides:** android-gsi-guide, custom-rom-notes, grapheneos-guide
