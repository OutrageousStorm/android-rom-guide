# Flashing Troubleshooting

## Boot loops
Flash recovery, wipe Dalvik/ART cache, re-flash ROM.

## Stuck on "Android is loading..."
Wait 15 minutes. If still stuck: wipe Dalvik in recovery.

## Signature verification failed
In TWRP: toggle "Zip signature verification" OFF at bottom.

## No sound
Audio HAL missing. Re-flash ROM or restore from backup.

## Bootloader locked
adb reboot bootloader
fastboot flashing unlock

## Stuck on "Initializing..."
System optimizing. Wait up to 20 minutes.
