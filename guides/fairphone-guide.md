# Fairphone Flashing Guide

Fairphone devices are highly modular and support multiple ROMs including CalyxOS, LineageOS, and e/OS.

## Device codenames

| Model | Codename | LineageOS | CalyxOS | e/OS |
|-------|----------|-----------|---------|------|
| Fairphone 3 | fp3 | ✅ 18-20 | ✅ | ✅ |
| Fairphone 3+ | fp3 | ✅ 18-20 | ✅ | ✅ |
| Fairphone 4 | fp4 | ✅ 19-21 | ✅ | ✅ |
| Fairphone 5 | fp5 | ✅ 21-22 | ⏳ | ⏳ |

## Bootloader unlock (Fairphone-specific)

Fairphone makes it EASY:

```bash
# 1. Enable OEM unlocking in Developer Options
adb reboot bootloader
fastboot oem unlock
# Device WILL wipe immediately
```

Unlike most OEMs, Fairphone's bootloader unlock is instant and straightforward.

## Flashing via fastboot

```bash
# FP4 with LineageOS 21
fastboot flash boot boot.img
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot -w
fastboot reboot
```

## Recovery

Most custom ROMs come with built-in recovery. TWRP also supports Fairphone:
```bash
fastboot flash recovery twrp.img
```

## Key advantages

- **Right to repair**: official spare parts program
- **Privacy-friendly ROMs available**: CalyxOS, e/OS, LineageOS
- **Long-term support**: security updates for 5+ years
- **Modular design**: easy to repair and upgrade
