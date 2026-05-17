# OTA Updates on Custom ROMs

How to receive and install OTA updates when running a custom ROM.

## LineageOS OTA

LineageOS updates come through the built-in Updater app:
```
Settings → About → System Update
```

Tap **Check for Updates**. If an OTA is available, you can download and install it directly without a computer.

**To preserve Magisk** after OTA:
```
Settings → Magisk Manager → Install → Install to Inactive Slot
# Then apply the OTA as normal
```

## Pixel (with GrapheneOS, CalyxOS, etc.)

Google still pushes OTA updates to Pixels. Some custom ROMs are based on AOSP and can receive them:

```bash
# Check for OTA
adb shell getprop ro.build.fingerprint

# Manual update via recovery
# 1. Reboot to recovery
# 2. Tap "Apply update from ADB"
# 3. adb sideload update.zip
```

## How to sideload updates

If OTA doesn't work automatically:

```bash
# 1. Get the update ZIP (from LineageOS mirrors, Pixel updates, etc.)
# 2. Reboot to recovery
adb reboot recovery

# 3. Select "Apply update from ADB"
# 4. Sideload
adb sideload update-filename.zip
```

## Preventing OTA interruption

Some devices nag about updates. Disable checks:

```bash
adb shell settings put global ota_disable 1
adb shell pm disable-user com.android.systemupdate
```

## Re-enable Magisk after OTA

If Magisk was removed by an OTA:
```bash
adb reboot bootloader
fastboot flash boot magisk_patched.img
fastboot reboot
```

---

**Note:** Always back up your data before OTA updates. See android-backup-vault.
