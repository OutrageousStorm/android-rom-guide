# Building Custom Vendor Images

The vendor partition holds device-specific drivers and firmware. Modifying it is the most powerful way to customize Android at the system level.

## What's in vendor?

```
/vendor/
├── bin/              # Device-specific daemons
├── lib/lib64/        # Native libs + HALs
├── etc/              # Config files
├── overlay/          # System overlay packages (replaces system UI resources)
├── firmware/         # Radio firmware, modem, Bluetooth, WiFi
├── build_id.txt      # Build identifier
└── app/              # System apps (OEM bloat)
```

## Extract vendor from device

```bash
# Find vendor partition
adb shell "ls -la /dev/block/by-name/ | grep vendor"

# Extract (requires root)
adb shell su -c "dd if=/dev/block/mmcblk0p<N> of=/sdcard/vendor.img"
adb pull /sdcard/vendor.img

# Or from OTA/ROM zip
unzip -p rom.zip vendor.img > vendor.img
```

## Repack vendor

```bash
# Mount and modify
mkdir vendor_mount
sudo mount -o loop vendor.img vendor_mount

# Remove OEM bloat
sudo rm -rf vendor_mount/app/SamsungKeychain
sudo rm -rf vendor_mount/priv-app/SamsungHealth
sudo rm -rf vendor_mount/lib/libsamsungdeeptranslate.so

# Remount RO and rebuild
sudo mount -o remount,ro vendor_mount
sudo umount vendor_mount

# Repack
e2fsck -f vendor.img
resize2fs vendor.img 500M  # shrink
```

## Flash vendor partition

```bash
adb reboot bootloader
fastboot flash vendor vendor.img
fastboot reboot
```

## Custom vendor overlays

Create system UI overlays in vendor:

```bash
vendor/overlay/
└── frameworks/
    └── base/
        └── core/res/
            └── res/
                ├── values/colors.xml      # Redefine system colors
                ├── values/dimens.xml      # Status bar height, etc
                └── drawable/              # Custom drawables
```

Rebuild and zip as overlay APK, place in `/vendor/overlay/`.

## Hardware abstraction layer (HAL) mods

HALs are in `/vendor/lib/hw/`. Common ones:

- `audio.primary.msm8974.so` — Audio routing, Dolby, speaker effects
- `lights.msm8974.so` — LED brightness, camera flash
- `power.msm8974.so` — CPU governor, thermal throttling
- `camera.msm8974.so` — Camera tuning

Replace with custom versions to unlock features or fix issues.

## Firmware updates

Firmware lives in `/vendor/firmware/`:

```bash
# Extract from device
adb shell su -c "find /vendor/firmware -type f | wc -l"  # count

# Update with newer versions
adb push new_firmware.bin /vendor/firmware/
adb shell chmod 644 /vendor/firmware/new_firmware.bin
```

Modem firmware changes can unlock bands or fix signal issues.

---

**Warning:** Vendor mods can brick if done wrong. Always keep a backup.
