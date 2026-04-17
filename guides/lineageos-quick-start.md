# LineageOS Quick Start

The most popular custom ROM — clean AOSP with frequent updates.

## Supported devices
200+ devices. Check: https://wiki.lineageos.org/devices/

## Install steps

1. **Unlock bootloader** (device-specific)
2. **Boot TWRP**: `adb reboot bootloader` → `fastboot boot twrp.img`
3. **Wipe**: Select **Advanced Wipe** → Dalvik/ART, Cache, System, Data
4. **Flash ROM**: Install → select `lineage-*.zip`
5. **Flash GApps** (optional): Install → select `arm64_gapps*.zip`
6. **Reboot system**

## First boot
- First boot takes 3-5 minutes
- Skip "Register device"
- Install F-Droid, get apps from there

## Common issues

**Stuck on boot logo**
- TWRP recovery still installed. Flash recovery.img from ROM zip via fastboot

**No WiFi/Bluetooth**
- Flashed wrong ROM for device codename. Check with: `adb shell getprop ro.build.fingerprint`

**Bootloader relocks after update**
- Some OEMs auto-relock. Use `fastboot oem unlock` again after OTA

## GApps alternatives
- **LineageOS for microG**: built-in microG (no Google)
- **Pico GApps**: minimal (just Play Store + Services)
- **NikGapps**: highly customizable package selection
