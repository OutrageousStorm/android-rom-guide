# Google Pixel 7 (panther) — ROM & Root Guide

> Released October 2022 · Tensor G2 · Android 13 → 15 · Security updates until October 2027

## Specifications

| | |
|---|---|
| Codename | panther |
| Chipset | Google Tensor G2 (Samsung 5nm) |
| RAM | 8 GB LPDDR5 |
| Storage | 128 / 256 GB UFS 3.1 |
| Display | 6.3" OLED 90Hz FHD+ |
| Battery | 4355 mAh |
| Camera | 50MP main + 12MP ultrawide |

## Bootloader Unlock

```bash
# 1. Enable Developer Options + OEM Unlocking
adb reboot bootloader
fastboot flashing unlock
# Confirm on-device — device wipes
```

## Root

### Magisk

```bash
# Download stock boot.img from:
# https://developers.google.com/android/images#panther
# Patch in Magisk app, then:
fastboot flash boot magisk_patched_*.img
fastboot reboot
```

### KernelSU

```bash
# Download from: https://github.com/tiann/KernelSU/releases
fastboot flash boot kernelsu_panther_*.img
fastboot reboot
# Install KernelSU Manager APK
```

## Custom ROMs

### GrapheneOS ⭐ (Best for Privacy)
- Official support ✅
- **Web install:** https://grapheneos.org/install/web (easiest)
- **CLI guide:** https://grapheneos.org/install/cli

### CalyxOS
- Official support ✅
- **Install:** https://calyxos.org/install/

### LineageOS 22.2 (Android 15)
- Official support ✅
```bash
# Flash recovery, then sideload:
fastboot flash recovery lineage_recovery_panther.img
fastboot reboot recovery
adb sideload lineage-22.2-*-panther.zip
```
- **Download:** https://download.lineageos.org/devices/panther
- **Guide:** https://wiki.lineageos.org/devices/panther/install

### Evolution X
- **Download:** https://evolution-x.org/device/panther

### crDroid
- **Download:** https://crdroid.net/panther

## Factory Images & OTA

- Factory images: https://developers.google.com/android/images#panther
- OTA images: https://developers.google.com/android/ota#panther
- XDA forum: https://forum.xda-developers.com/f/google-pixel-7.12607/
