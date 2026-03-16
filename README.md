# 📖 Android ROM Guide

> **The definitive guide to flashing custom ROMs on Android.** Covers bootloader unlocking, Magisk/KernelSU root, and all major ROMs for Pixel, Samsung, Xiaomi, and OnePlus devices.

[![License](https://img.shields.io/badge/license-CC--BY--SA%204.0-blue)](LICENSE)
[![Devices](https://img.shields.io/badge/devices-50%2B-brightgreen)](#devices)
[![ROMs](https://img.shields.io/badge/ROMs%20covered-10%2B-orange)](#roms)
[![Stars](https://img.shields.io/github/stars/OutrageousStorm/android-rom-guide?style=social)](https://github.com/OutrageousStorm/android-rom-guide/stargazers)

---

## 📌 Quick Navigation

- [🔓 Bootloader Unlock (Universal)](#bootloader-unlock)
- [🔑 Root: Magisk vs KernelSU](#root)
- [📱 Device Guides](#devices)
- [🌐 ROM Comparison](#rom-comparison)
- [⚠️ FAQ & Troubleshooting](#faq)

---

## 🔓 Bootloader Unlock

> ⚠️ **Warning:** Unlocking the bootloader **factory resets your device**. Back up everything first.

### Prerequisites

1. Install [ADB & Fastboot](https://developer.android.com/tools/releases/platform-tools)
2. Enable **Developer Options**: Settings → About Phone → tap **Build Number** 7 times
3. Enable **OEM Unlocking**: Developer Options → OEM Unlocking ✓
4. Enable **USB Debugging**: Developer Options → USB Debugging ✓

### Universal Fastboot Unlock (Pixel, most Android One)

```bash
adb reboot bootloader
fastboot flashing unlock
# Confirm on device — phone wipes and reboots
```

### Samsung (Exynos & Snapdragon)

Samsung requires a different approach — see the [Samsung guide](devices/samsung/).

**Note:** Snapdragon Samsung devices (US models) cannot unlock the bootloader through normal means. Exynos variants support it.

### Xiaomi

Xiaomi requires a waiting period (7 days) after requesting unlock permission via their [Mi Unlock Tool](https://en.miui.com/unlock/).

```bash
# After unlock permission is granted:
adb reboot bootloader
fastboot flashing unlock   # or: fastboot oem unlock (older devices)
```

### OnePlus

```bash
adb reboot bootloader
fastboot oem unlock    # Older devices
# or
fastboot flashing unlock  # Newer OxygenOS 12+
```

---

## 🔑 Root

### Magisk (Most Compatible)

Magisk is the go-to root solution, supporting thousands of modules and most apps.

```bash
# 1. Download stock boot.img for your exact build
# 2. Transfer to phone, patch via Magisk app:
#    Install → Select and Patch a File
# 3. Transfer patched image back to PC
adb pull /sdcard/Download/magisk_patched_*.img .

# 4. Flash
fastboot flash boot magisk_patched_*.img
fastboot reboot
```

- [Magisk GitHub](https://github.com/topjohnwu/Magisk)
- [Magisk Modules Repo](https://github.com/Magisk-Modules-Alt-Repo)

### KernelSU (Kernel-Level, Harder to Detect)

KernelSU operates at the kernel level — more secure, harder for apps (banking, DRM) to detect.

```bash
# Download KernelSU boot image for your device codename
fastboot flash boot kernelsu_[codename]_*.img
fastboot reboot
# Install KernelSU Manager APK
```

- [KernelSU GitHub](https://github.com/tiann/KernelSU)
- Better for: hiding root from banking/DRM apps
- Works on: most GKI-compatible devices (Android 12+)

### Hiding Root

| Method | Tool | Notes |
|---|---|---|
| Magisk DenyList | Built-in Magisk | Works for most apps |
| Shamiko module | [Shamiko](https://github.com/LSPosed/LSPosed.github.io/releases) | Advanced hide, install as Magisk module |
| KernelSU | KernelSU + ZygiskNext | Strongest hide |

---

## 📱 Devices

### Google Pixel

| Device | Codename | Bootloader | Magisk | KernelSU | LineageOS | GrapheneOS |
|---|---|---|---|---|---|---|
| Pixel 5 | redfin | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 6 | oriole | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 6 Pro | raven | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 7 | panther | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 7 Pro | cheetah | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 8 | shiba | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 8 Pro | husky | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |
| Pixel 9 | tokay | ✅ | ✅ | ✅ | ✅ 22.2 | ✅ |

📄 **Detailed guides:** [devices/pixel/](devices/pixel/)

### Samsung Galaxy

| Device | Chipset | Bootloader | Root | LineageOS |
|---|---|---|---|---|
| Galaxy S10 (beyond1lte) | Exynos 9820 | ✅ Exynos | ✅ | ✅ 21.x |
| Galaxy S20 (x1s) | Exynos 990 | ✅ Exynos | ✅ | ✅ 21.x |
| Galaxy S21 (o1s) | Exynos 2100 | ✅ Exynos | ✅ | ✅ 22.x |
| Galaxy S22 (r0s) | Exynos 2200 | ✅ Exynos | ✅ | ✅ 22.x |
| Galaxy A52s (a52sxq) | SD 778G | ✅ | ✅ | ✅ 22.x |

📄 **Detailed guides:** [devices/samsung/](devices/samsung/)

### Xiaomi / Redmi

| Device | Codename | Bootloader | Root | LineageOS |
|---|---|---|---|---|
| Redmi Note 9 Pro | joyeuse | ✅ (7-day wait) | ✅ | ✅ 21.x |
| POCO F4 | munch | ✅ | ✅ | ✅ 22.x |
| Redmi Note 12 Pro | ruby | ✅ | ✅ | ✅ 22.x |
| Xiaomi 12 | cupid | ✅ | ✅ | ✅ 22.x |

📄 **Detailed guides:** [devices/xiaomi/](devices/xiaomi/)

### OnePlus

| Device | Codename | Bootloader | Root | LineageOS |
|---|---|---|---|---|
| OnePlus 8 Pro | instantnoodlep | ✅ | ✅ | ✅ 22.x |
| OnePlus 9 Pro | lemonadep | ✅ | ✅ | ✅ 22.x |
| OnePlus 12 | aston | ✅ | ✅ | ⚠️ Unofficial |

📄 **Detailed guides:** [devices/oneplus/](devices/oneplus/)

---

## 🌐 ROM Comparison

| ROM | Base | GApps | Privacy | Stability | Pixel UI | Active? |
|---|---|---|---|---|---|---|
| **GrapheneOS** | AOSP | Optional (sandboxed) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ |
| **CalyxOS** | AOSP | microG | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ✅ |
| **LineageOS** | AOSP | No (add manually) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ |
| **PixelExperience** | AOSP | Yes | ⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **crDroid** | AOSP | No | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ✅ |
| **Evolution X** | AOSP | Yes | ⭐⭐ | ⭐⭐⭐ | ✅ | ✅ |
| **Paranoid Android** | AOSP | Optional | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ |
| **ArrowOS** | AOSP | Optional | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ✅ |

> **Recommendation:**
> - **Maximum privacy:** GrapheneOS (Pixel only)
> - **Privacy + app compatibility:** CalyxOS
> - **Most devices + stable:** LineageOS
> - **Pixel UI feel everywhere:** PixelExperience
> - **Heavy customization:** crDroid or Evolution X

---

## ❓ FAQ

**Q: Will I lose data when unlocking the bootloader?**
> Yes — bootloader unlock triggers a factory reset. Back up everything with `adb backup` or Google backup first.

**Q: Can I go back to stock firmware?**
> Yes. Flash the official factory image via fastboot. All Pixel factory images are at [developers.google.com/android/images](https://developers.google.com/android/images).

**Q: Will banking apps work after rooting?**
> With Magisk DenyList or Shamiko, most banking apps work fine. KernelSU is even better at hiding root.

**Q: Is my warranty voided?**
> Technically yes, but you can restore stock firmware before sending for warranty service.

**Q: What's the difference between KernelSU and Magisk?**
> Magisk works in userspace (patches boot image). KernelSU is built into the kernel. KernelSU is harder for apps to detect, but has less module support currently.

---

## 📚 More Resources

- 📖 [ROM Haven Wiki](https://romhaven.wikioasis.org) — device-specific ROM guides
- 💬 [XDA Forums](https://xda-developers.com) — community support
- 🔧 [Android Tweaks Toolkit](https://github.com/OutrageousStorm/android-tweaks-toolkit) — debloat & ADB tools
- 🔒 [Android Privacy Hardener](https://github.com/OutrageousStorm/android-privacy-hardener) — harden without root

---

## 🤝 Contributing

Device guides, ROM additions, and corrections are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

*Maintained by [Tom](https://github.com/OutrageousStorm) · Android Intelligence · CC BY-SA 4.0*
