# Android Modem/Firmware Flashing

How to flash modem firmware separately from ROM — needed when switching to custom ROM on same device.

## Why flash modem?

- Custom ROMs sometimes don't include updated modem firmware
- Modem controls signal, connectivity, call quality
- Flashing a new modem can improve signal or fix network issues
- Device-specific — varies by manufacturer and variant

## Get modem firmware

```bash
# From factory image (Pixel)
unzip device-factory-image.zip
cd $DEVICE-$BUILD
ls *.img | grep -i modem
# Look for: modem.img, NON-HLOS.bin, NON-HLOS.mbn, firmware.img

# Samsung (from firmware.zip or stock Odin flashable)
ls AP_*.tar.md5
# Contains modem firmware in ABOOT, BOOT, SYSTEM partitions
```

## Flash via fastboot

```bash
# Pixel / Generic
fastboot flash modem modem.img
fastboot flash vendor vendor.img
fastboot reboot bootloader
fastboot flash system system.img

# Variant: SOC-specific
fastboot getvar variant
fastboot flash modem_$VARIANT modem.img
```

## Flash via TWRP

```bash
# If TWRP provides firmware flasher:
adb push modem.img /sdcard/
# In TWRP: Advanced → Flash firmware → select modem.img
```

## Restore original modem

```bash
# From stock firmware
adb reboot bootloader
fastboot flash modem modem.img  # from factory image
fastboot reboot
```

## Modem partition names

| Device | Modem partition | Alternative |
|--------|-----------------|-------------|
| Pixel | modem | NON-HLOS.bin |
| OnePlus | modem | splash |
| Samsung | (in AP) | boot, vendor |
| Xiaomi | vendor_boot | splash |
| Motorola | vendor | vendor_boot |

**Note:** Do NOT flash modem to boot partition — always verify the correct partition for your device.
