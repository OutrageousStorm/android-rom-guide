# Google Pixel 8 (shiba) — ROM & Root Guide

> Released October 2023 · Tensor G3 · Android 14 → 15 · Updates until October 2031 (7 years!)

## Specifications

| | |
|---|---|
| Codename | shiba |
| Chipset | Google Tensor G3 (Samsung 4nm) |
| RAM | 8 GB LPDDR5X |
| Storage | 128 / 256 GB UFS 3.1 |
| Display | 6.2" OLED 120Hz FHD+ |
| Battery | 4575 mAh |

## Bootloader Unlock

```bash
adb reboot bootloader
fastboot flashing unlock
```

## Root

### Magisk
```bash
# Get boot.img: https://developers.google.com/android/images#shiba
fastboot flash boot magisk_patched_*.img && fastboot reboot
```

### KernelSU
```bash
fastboot flash boot kernelsu_shiba_*.img && fastboot reboot
```

## ROMs

| ROM | Status | Link |
|---|---|---|
| GrapheneOS | ✅ Official | https://grapheneos.org/install/web |
| CalyxOS | ✅ Official | https://calyxos.org/install/ |
| LineageOS 22.2 | ✅ Official | https://download.lineageos.org/devices/shiba |
| Evolution X | ✅ Official | https://evolution-x.org/device/shiba |
| crDroid | ✅ Official | https://crdroid.net/shiba |

## Factory Images

- https://developers.google.com/android/images#shiba
- XDA: https://forum.xda-developers.com/f/google-pixel-8.12607/
