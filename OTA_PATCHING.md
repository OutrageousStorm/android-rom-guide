# Patching Android OTA Updates

Keep root and custom mods alive through OTA updates.

## The OTA format

```
OTA.zip
├── META-INF/
│   ├── MANIFEST.MF
│   ├── CERT.SF
│   └── CERT.RSA
├── system/
├── vendor/
├── recovery/
└── boot.img  (or init_boot.img on A/B devices)
```

## Extract and modify

```bash
unzip OTA.zip
adb push system system/
# Modify files...
adb pull system system_modified/
```

## Re-sign OTA

The update must be signed with a key the device trusts. For testing:

```bash
# Download AOSP signing tools
git clone https://android.googlesource.com/platform/build

# Sign
python3 sign_target_files.py -d ~/.android/testkey.pk8 \
  input.target_files output.target_files

python3 ota_from_target_files.py output.target_files custom_OTA.zip
```

## Magisk + OTA survival

Magisk can patch OTA *before* installation:

1. Download OTA
2. Open Magisk app → Install → **Install to Inactive Slot (After OTA)**
3. Let OTA download and validate
4. Magisk patches boot partition in the inactive slot
5. Reboot → update takes effect with root intact

This is the **safest way** to survive OTA updates.

## Manual flash method

If OTA fails or you need full control:

```bash
# Extract from OTA.zip
unzip OTA.zip system.img vendor.img boot.img vbmeta.img

# Boot to fastbootd
adb reboot fastboot

# Flash manually
fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash boot boot.img
fastboot flash vbmeta --disable-verity --disable-verification vbmeta.img
fastboot reboot
```

---

Magisk's built-in OTA survival is the best approach for rooted users.
