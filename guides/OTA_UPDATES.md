# Handling OTA Updates on Custom ROMs

How to apply OTA updates safely while keeping root/Magisk.

## Prerequisites
- Rooted with Magisk
- Original boot.img for your ROM version (in case of emergency)

## Method 1: Magisk Install-to-Inactive-Slot (easiest)

Most ROMs with A/B partitions support applying OTA to the inactive slot.

```bash
# 1. OTA notification appears — DON'T install yet
# 2. Open Magisk Manager → Install → Install to Inactive Slot (After OTA)
# 3. System will prompt for OTA confirmation
# 4. Choose "Install"
# 5. Magisk patches the new slot automatically
# 6. Reboot to apply

# If it fails, fall back to Method 2
```

## Method 2: Manual patching after OTA

```bash
# 1. Let OTA download fully (Settings → System → System Update)
# 2. Reboot to recovery but DON'T install yet
# 3. On PC:
adb pull /dev/block/by-name/boot_b boot_new.img  # pull the new inactive slot
# 4. Patch with Magisk:
# Open Magisk APK on phone, select boot_new.img, patch it
# 5. Flash patched image:
adb push magisk_patched_*.img /sdcard/
adb reboot bootloader
fastboot flash boot magisk_patched_*.img
fastboot reboot
```

## Method 3: Block OTA temporarily

If you're not ready to update:

```bash
# Disable OTA notification
adb shell settings put global system_update_setting 0

# Or block the updater app entirely
adb shell pm disable-user --user 0 com.android.systemupdate
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| OTA fails to install | Boot to recovery, sideload old OTA first to get back in sync |
| Boot loop after OTA | Boot to recovery, flash original boot.img, re-root |
| Magisk gone after OTA | Expected if you didn't use Install-to-Inactive-Slot — re-patch boot.img |

## Recovery after failed OTA

```bash
# If stuck in boot loop
adb reboot recovery
# In TWRP: Wipe → Dalvik Cache, then reboot

# If that fails, sideload the ROM
adb sideload rom.zip
```
