# Samsung Galaxy S23 (r0q/dm1q) — ROM & Root Guide

> Released February 2023 · Snapdragon 8 Gen 2 (US/global) or Exynos 2200 (some regions)

## ⚠️ Important: Snapdragon vs Exynos

| Variant | Chipset | Bootloader Unlock | Root | Custom ROMs |
|---|---|---|---|---|
| US / Global (SM-S911U/B) | Snapdragon 8 Gen 2 | ❌ Locked | ❌ Very limited | ❌ Very limited |
| Some EU/KR (SM-S911B) | Exynos 2200 | ✅ | ✅ | ✅ |

> **US Galaxy S23 users:** Samsung locks the bootloader on US Snapdragon variants. Root via official means is not currently possible. Consider using **Shizuku** for no-root system access instead.

## Specifications

| | |
|---|---|
| US Codename | r0q |
| EU Codename | dm1q |
| Chipset (US) | Snapdragon 8 Gen 2 |
| Chipset (EU/KR) | Exynos 2200 |
| RAM | 8 GB LPDDR5X |
| Storage | 128 / 256 GB UFS 3.1 |
| Display | 6.1" Dynamic AMOLED 120Hz FHD+ |
| Battery | 3900 mAh |

## Exynos Variant: Bootloader Unlock

```bash
# Enable Developer Options + OEM Unlocking
adb reboot bootloader
fastboot oem unlock
# Confirm on device — wipes phone
```

## Exynos Variant: Root (Magisk)

1. Download stock firmware for your exact CSC from [SamFW](https://samfw.com) or [SamMobile](https://sammobile.com)
2. Extract the AP_*.tar.md5 and find `boot.img.lz4`
3. Decompress: `unlz4 boot.img.lz4 boot.img`
4. Transfer to phone, patch via Magisk app
5. Flash patched boot image via Odin or Heimdall

## Custom Recoveries (Exynos)

- **TWRP:** [Official build for dm1q](https://twrp.me/samsung/samsunggalaxys23.html)
- **OrangeFox:** Unofficial — check XDA thread

## Custom ROMs (Exynos)

| ROM | Status | Link |
|---|---|---|
| LineageOS 21 | ✅ Official (dm1q) | https://download.lineageos.org/devices/dm1q |
| crDroid | ✅ Official | https://crdroid.net/dm1q |
| Evolution X | ✅ Official | https://evolution-x.org/device/dm1q |

## Snapdragon Alternatives (No Root)

Since US S23 can't be rooted, use these instead:

- **[Shizuku](https://shizuku.rikka.app/)** — ADB-level access without root
- **[Android Privacy Hardener](https://github.com/OutrageousStorm/android-privacy-hardener)** — Privacy via ADB
- **[Android Tweaks Toolkit](https://github.com/OutrageousStorm/android-tweaks-toolkit)** — Debloat via ADB

## Resources

- XDA S23 Forum: https://forum.xda-developers.com/f/samsung-galaxy-s23.12579/
- SamFW Firmware: https://samfw.com/firmware/SM-S911B
