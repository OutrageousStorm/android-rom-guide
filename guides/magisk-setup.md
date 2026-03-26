# Magisk Setup Guide

The complete guide to installing and configuring Magisk root.

**GitHub:** https://github.com/topjohnwu/Magisk

---

## What is Magisk?

Magisk is a **systemless root** solution — it modifies the system in memory rather than on disk. This means:
- OTA updates survive (just need to re-patch boot.img after)
- Root is harder to detect (no `/system` modifications)
- Modules can be cleanly removed
- Zygisk enables deep app-level hooking

---

## Install method 1: Patch boot.img (recommended)

```bash
# 1. Download Magisk APK from https://github.com/topjohnwu/Magisk/releases
# 2. Install the APK on your device
# 3. Extract boot.img from your ROM zip
#    (or download factory image matching your exact build)

# 4. Transfer boot.img to device
adb push boot.img /sdcard/

# 5. In Magisk app: Install → Select and Patch a File → pick boot.img
#    Output: /sdcard/Download/magisk_patched_xxxxx.img

# 6. Pull patched image
adb pull /sdcard/Download/magisk_patched_xxxxx.img ./

# 7. Flash it
adb reboot bootloader
fastboot flash boot magisk_patched_xxxxx.img
fastboot reboot
```

---

## Install method 2: Via custom recovery

```bash
# In TWRP recovery:
# Install → navigate to Magisk.apk → rename to Magisk.zip → install
# Reboot system
```

---

## Post-install setup

1. Open Magisk app — grant it root if prompted
2. Enable **Zygisk** (Settings → Zygisk → On)
3. Configure **DenyList** for banking/payment apps:
   - Settings → Configure DenyList
   - Check: your banking app, Google Pay, etc.
4. Reboot

---

## Essential first modules

```
PlayIntegrityFix  — pass Google's hardware attestation check
LSPosed           — Xposed framework for deep system hooks
Shamiko           — advanced root hiding (requires Zygisk)
```

Install via Magisk → Modules → search, or install from zip.

---

## Survive OTA updates (LineageOS / Pixel)

```bash
# After OTA downloads but before applying:
# 1. Open Magisk → Install → Install to Inactive Slot (After OTA)
# 2. Apply the OTA update
# Magisk patches the new slot automatically
```

---

## Uninstall Magisk (cleanly)

```bash
# Magisk app → Uninstall → Complete Uninstall
# This restores the original boot.img and removes all traces
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Boot loop after install | Boot to recovery, flash original boot.img |
| App detects root | Enable DenyList for that app, install Shamiko |
| Module causes boot loop | Boot to recovery → Magisk → disable all modules |
| SafetyNet/Play Integrity fails | Install PlayIntegrityFix + TrickyStore |
