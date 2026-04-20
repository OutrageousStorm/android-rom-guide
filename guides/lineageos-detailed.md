# LineageOS — Complete Setup & Building Guide

## Installation

### Finding your device

1. Go to https://wiki.lineageos.org/devices/
2. Search for your device codename
3. Download the latest stable build

### Pre-install checklist

```bash
adb reboot bootloader
fastboot getvar current-slot        # Check A/B slot status
fastboot oem unlock                 # Unlock bootloader (wipes data!)
# After unlock, device reboots to bootloader automatically
```

### Flashing

```bash
fastboot flash boot lineage-*.boot.img
fastboot flash system lineage-*.system.img  # or system.img for A-only
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot -w                         # Wipe userdata
fastboot reboot
```

Or via TWRP recovery (sideload):
```bash
adb sideload lineage-*.zip
adb sideload lineage-microG-*.zip   # if using microG
adb sideload magisk.zip             # if rooting
```

## Post-install

### Essential first steps
1. **Skip Google Setup** if not using GApps
2. **Enable Developer Options** (Settings → About → Build Number ×7)
3. **Enable USB Debugging**
4. **Set location mode** (Privacy → Location)

### GApps or microG?

**GApps** — Full Google services (Play Store, Drive, Maps, etc.)
- Download MindTheGapps matching your Android version
- Flash via TWRP or sideload after ROM

**microG** — Lightweight alternative (Privacy-focused)
- Some apps work, some don't (depends on which Play APIs they use)
- LineageOS for microG: official LineageOS build with microG pre-installed
- https://lineage.microg.org

### Magisk root (optional)

```bash
# Download latest from https://github.com/topjohnwu/Magisk
adb push Magisk-v25.2.apk /sdcard/
adb install /sdcard/Magisk-v25.2.apk
# Open Magisk app, tap Install → Select and Patch a File
# Choose boot.img or recovery partition as source
# Flash patched image via fastboot
```

## Building LineageOS from source

### Requirements

```bash
# Linux (Ubuntu 20.04+)
sudo apt install git-core gnupg flex bison gperf build-essential   zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386   lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev   libgl1-mesa-dev libxml2-utils xsltproc unzip python3

# Disk space: 200+ GB
# RAM: 16GB+ recommended
```

### Sync & build

```bash
mkdir ~/lineage && cd ~/lineage

# Initialize repo
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0

# Sync (takes 1-2 hours on good connection)
repo sync -j$(nproc) --force-sync

# Lunch and build for your device (e.g., sunfish = Pixel 4a)
. build/envsetup.sh
lunch lineage_sunfish-user
mka bacon -j$(nproc)

# Output: out/target/product/sunfish/lineage-*.zip
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No such file or directory" on boot | Wrong boot partition — check A/B layout |
| TWRP can't mount /system | Disable verified boot with vbmeta wipe |
| GApps won't install | Install to non-encrypted /system (TWRP → Format) |
| Play Integrity fails | Install PlayIntegrityFix + TrickyStore Magisk modules |
| Bootloader locked after update | Reboot to recovery, re-unlock via fastboot |

## Resources

- **Official**: https://wiki.lineageos.org
- **XDA Forums**: https://forum.xda-developers.com/c/lineageos.7621
- **GitHub**: https://github.com/LineageOS
