# OnePlus Flashing Guide

OnePlus has historically been one of the most dev-friendly OEMs with easy bootloader unlock and great custom ROM support.

---

## Bootloader unlock

OnePlus has the simplest unlock process of any major OEM:

```bash
# Enable Developer Options → OEM Unlocking
adb reboot bootloader
fastboot oem unlock   # older OnePlus (OP6 and below)
fastboot flashing unlock  # newer OnePlus (OP7+)
```

No waiting period. No account linking. Instant.

> ⚠️ OnePlus 10+ may have carrier variants with locked bootloaders (T-Mobile). Verify before buying for modding.

---

## OxygenOS vs ColorOS

From OnePlus 10 onwards, OnePlus merged with OPPO and shifted to **ColorOS** base instead of OxygenOS:
- OxygenOS 12 (OP9 and below): Stock Android feel, minimal bloat
- OxygenOS 13+ (OP10+): ColorOS base, more Chinese-style features
- Community strongly prefers LineageOS on newer OnePlus

---

## A/B partitions

All OnePlus devices from OP5 onwards use A/B partitions:

```bash
# Flash to current slot
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img

# Or let the ROM installer handle it via recovery
```

---

## Popular OnePlus ROMs

| Device | Top ROM picks |
|--------|--------------|
| OnePlus 6 (enchilada) | LineageOS 21, crDroid, Paranoid Android |
| OnePlus 7 Pro (guacamole) | LineageOS 21, Evolution X |
| OnePlus 8 Pro (instantnoodlep) | LineageOS 21, crDroid |
| OnePlus 9 Pro (lemonadep) | LineageOS 21, PixelOS |
| OnePlus 10 Pro (harobed) | LineageOS 21, crDroid |
| OnePlus Nord (avicii) | LineageOS 20, crDroid |
| OnePlus Nord 2 (denniz) | LineageOS 20 |

---

## Fastboot tips

```bash
# Check current slot
fastboot getvar current-slot

# Switch slot
fastboot set_active other

# Flash vbmeta to disable verified boot
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
```

---

*Device pages: [ROM Haven wiki](https://romhaven.wikioasis.org)*
