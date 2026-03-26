# GApps Guide — Google Apps for Custom ROMs

Custom ROMs ship without Google apps by default. Here's how to add them.

---

## Do you need GApps?

| Scenario | GApps needed? |
|----------|--------------|
| Using GrapheneOS | No — has Sandboxed Play built-in |
| Using CalyxOS | No — has microG built-in |
| Using LineageOS for microG | No — microG is included |
| Using LineageOS / crDroid / Evolution X | Yes, if you want Google apps |
| Full de-Google setup | No — use F-Droid + Aurora Store |

---

## GApps providers

### MindTheGapps (recommended)
- Clean, maintained, works well with LineageOS
- Download: https://mindthegapps.com
- Match your Android version and architecture (arm64 for modern phones)

### NikGapps
- Highly customizable — choose exactly which Google apps to include
- Download: https://nikgapps.com

### BiGGapps
- Another solid option
- Download: https://downloads.bigota.net

---

## Package sizes

| Package | Includes | Size |
|---------|---------|------|
| **pico** | Play Store + Play Services only | ~250MB |
| **nano** | + Google Search, Gmail (lite) | ~350MB |
| **micro** | + Gmail full, Maps | ~500MB |
| **mini** | + YouTube, Drive | ~700MB |
| **full** | Complete Google suite | ~1GB+ |

**Recommendation:** Start with `pico` — install individual apps from Play Store as needed.

---

## Flash order (critical!)

Always flash in this order:
1. Wipe data (if clean install)
2. Flash **ROM** zip
3. Flash **GApps** zip (before first boot)
4. Flash **Magisk** zip (if rooting)
5. Reboot

> ⚠️ Flashing GApps after first boot may fail or cause boot loops. Always flash before first boot.

---

## Architecture check

```bash
adb shell getprop ro.product.cpu.abi
# arm64-v8a = arm64 (most modern phones)
# armeabi-v7a = arm (older 32-bit)
# x86_64 = x86_64 (emulators, some Atoms)
```

---

## Alternative: microG

microG is an open-source reimplementation of Google Play Services. It allows Google-dependent apps to function without full Google Play Services.

- Less data sent to Google
- Open source and auditable
- Some apps work, some don't (depends on which Play Services API they use)

**LineageOS for microG:** https://lineage.microg.org  
**microG standalone:** https://microg.org
