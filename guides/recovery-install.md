# Installing Recovery Images

How to flash custom recovery (TWRP, OrangeFox, Lineage Recovery).

## Via fastbootd (recommended)

```bash
# Boot to fastbootd (NOT regular fastboot)
adb reboot fastboot

# Flash recovery
fastboot flash recovery recovery.img

# Optional: flash boot.img too for A/B devices
fastboot flash boot boot.img

# Reboot to recovery
fastboot reboot recovery
```

## Via ADB sideload

```bash
# Boot to recovery
adb reboot recovery

# Sideload recovery.zip
adb sideload recovery.zip
```

## Verify flash

```bash
# Check boot version
adb shell getprop ro.bootimage.build.date

# Verify recovery
adb shell sha256sum /dev/block/by-name/recovery
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Recovery not found | Use correct partition name |
| Boot loop | Flash original recovery, try again |
| Fastbootd not found | Device doesn't support A/B, use ADB sideload |
