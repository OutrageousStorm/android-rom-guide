# Bootloader Unlock & Fastboot

Understanding the bootloader — the firmware that runs before Android kernel loads.

## What is the bootloader?

The bootloader is low-level firmware that initializes hardware and loads the kernel. On Android:
- **Bootloader** = runs before kernel, loads boot partition
- **Fastboot** = protocol to communicate with bootloader from PC
- **Fastbootd** = userspace fastboot in recovery (for large partitions like system)

## Check bootloader state

```bash
# Device-side
adb shell getprop ro.boot.verifiedbootstate
# Output: green (locked), yellow (custom build), orange (unlocked), red (error)

# Fastboot-side
fastboot getvar all | grep "bootloader"
```

## Unlock (erases data)

```bash
adb reboot bootloader
fastboot flashing unlock
# Device will wipe /data
fastboot reboot
```

## Lock again

```bash
adb reboot bootloader
fastboot flashing lock
```

## Fastboot vs fastbootd

| Command | Boot mode | Use case |
|---------|-----------|----------|
| `fastboot flash boot ...` | Bootloader | Flash kernel, recovery, small partitions |
| `adb reboot fastboot` then `fastboot flash system ...` | Fastbootd | Flash large partitions (system, product, vendor) |

## Flash a custom ROM via fastboot

```bash
# 1. Unlock bootloader (if needed)
fastboot flashing unlock

# 2. Boot to fastbootd (not regular fastboot)
adb reboot fastboot

# 3. Erase system
fastboot erase system

# 4. Flash the ROM
fastboot flash system rom.img

# 5. Flash vbmeta with verification disabled
fastboot flash vbmeta --disable-verity --disable-verification vbmeta.img

# 6. Wipe userdata
fastboot -w

# 7. Reboot
fastboot reboot
```

See also: [[GSI Flashing]], [[Magisk Patching]]
