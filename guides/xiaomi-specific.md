# Xiaomi / POCO / Redmi Flashing Guide

Xiaomi has a unique bootloader unlock process with mandatory waiting periods.

---

## The unlock wait

Xiaomi requires you to:
1. Apply for bootloader unlock at https://unlock.mi.com
2. Wait **30 days** (China units) or **72 hours** (global units) before unlocking
3. During this time, the device must be connected to a Mi Account with an active SIM

This is enforced server-side — cannot be bypassed without modification.

---

## Unlock process

```bash
# 1. Log into Mi Account on device
# 2. Enable Developer Options → Mi Unlock Status → Add account
# 3. Download Mi Unlock Tool (Windows only): https://unlock.mi.com
# 4. Reboot to fastboot: adb reboot bootloader
# 5. Open Mi Unlock Tool, sign in, click Unlock
```

---

## Fastboot commands (standard)

```bash
fastboot flash recovery twrp.img
fastboot boot twrp.img           # temp boot recovery
fastboot flash boot boot.img
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot reboot
```

---

## A/B vs A-only partitions

Recent Xiaomi devices (POCO F3, Redmi Note 11+) use **A/B partition scheme**:
- No dedicated recovery partition
- TWRP flashed to boot/recovery partition
- Use `fastboot boot twrp.img` to temp boot, then install

Older devices (Redmi Note 7, POCO F1) use **A-only**:
- Dedicated recovery partition
- Flash directly with `fastboot flash recovery twrp.img`

---

## HyperOS / MIUI notes

- HyperOS (Xiaomi's MIUI successor) has stricter GMS checks
- Some HyperOS builds detect custom recoveries more aggressively
- LineageOS / crDroid recommended for clean daily drivers

---

## Popular Xiaomi ROMs

| Device | Recommended ROM |
|--------|----------------|
| POCO F3 (alioth) | LineageOS 21, crDroid, Evolution X |
| POCO F4 (munch) | LineageOS 21, Pixel Experience |
| Redmi Note 10 Pro (sweet) | crDroid, LineageOS |
| Redmi Note 12 Pro 5G (ruby) | LineageOS 21, PixelOS |
| Xiaomi 12 (cupid) | LineageOS 21, crDroid |

---

*Device pages: [ROM Haven wiki](https://romhaven.wikioasis.org)*
