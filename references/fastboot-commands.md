# Fastboot Command Reference

Quick reference for all fastboot commands used in ROM flashing.

## Connections & devices

```bash
fastboot devices                    # list connected devices
fastboot reboot bootloader          # reboot to fastboot mode
fastboot reboot recovery            # reboot to recovery
fastboot reboot                     # normal reboot
```

## Flashing partitions

```bash
# Single-file flashing
fastboot flash boot boot.img
fastboot flash recovery recovery.img
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash product product.img
fastboot flash vbmeta vbmeta.img

# A/B devices (two slots)
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img
fastboot flash system_a system.img
fastboot flash system_b system.img

# Bulk flash with images zip
fastboot update image.zip
fastboot -w update image.zip        # wipe data too
```

## Wiping & erasing

```bash
fastboot erase boot
fastboot erase system
fastboot erase userdata
fastboot erase cache
fastboot erase -w                   # wipe everything
```

## Bootloader & security

```bash
fastboot flashing unlock            # unlock bootloader (wipes data)
fastboot flashing lock              # lock bootloader again
fastboot flashing lock_critical     # critical lock

fastboot getvar is-userspace        # check partition scheme
fastboot getvar current-slot        # check A/B slot
fastboot set_active other           # switch to other A/B slot
```

## Partition verification

```bash
fastboot getvar all                 # show all device vars
fastboot getvar product             # device codename
fastboot getvar partition-type:system
fastboot oem getvar bootloader      # bootloader version
```

## Advanced

```bash
# Disable verified boot (warning: security risk)
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Boot without flashing (temp boot)
fastboot boot recovery.img          # NOT the same as flash

# Super partition (dynamic partitions)
fastboot flash super super.img       # A/B devices with dynamic partitions
```

## Troubleshooting

```bash
# Device in fastbootd (not fastboot)?
fastboot -l                         # use long transport timeout
fastboot --skip-validation          # skip validation check

# Stuck? Force reset
fastboot reboot bootloader
# Then try again
```
