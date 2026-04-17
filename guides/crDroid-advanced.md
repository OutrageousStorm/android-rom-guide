# crDroid Advanced Guide

crDroid = heavily customized LineageOS with hundreds of extra tweaks.

## Key differences from LineageOS

crDroid includes:
- Custom Bluetooth codecs (LDAC, aptX, LHDC)
- Per-app language override
- Extended notification options
- Custom charging animations
- Navbar customizer with multiple layouts
- Standalone clock styles
- Lockscreen shortcuts
- Gaming mode with CPU lock
- Persistent RAM swap
- Automatic brightness curve adjustment

## Installation
Same as LineageOS, but often includes GApps in the package.

```
1. TWRP → Wipe (System, Data, Cache, Dalvik)
2. Flash crDroid.zip
3. Flash crDroid-Gapps.zip (if included)
4. Reboot
```

## First boot tweaks

Settings → System:
- **Standalone Clocks** → pick your lock/AOD style
- **Lockscreen** → add shortcuts (camera, flashlight, etc)
- **Navigation** → Navbar tweaker for button layouts
- **Gaming Mode** → CPU clock + disable notifications
- **Performance** → RAM swap, zRAM size, I/O scheduler

## Gboard alternatives in crDroid

crDroid's defaults:
- **Keyboard**: Gboard (you can replace with OpenBoard, FUTO, etc)
- **Launcher**: Trebuchet with extra customization
- **Gallery**: AOSP Gallery (Pixels use Google Photos)

## Known crDroid quirks

- Updates every 2-3 days (frequent)
- Some devices may have untested features
- Requires 8GB+ RAM for optimal performance with all tweaks enabled

Device support: https://crdroid.net/
