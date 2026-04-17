# Building LineageOS from Source

Guide to compiling LineageOS from source for your device.

## Requirements
- Linux (Ubuntu 20.04+)
- 200GB+ free space
- 16GB+ RAM recommended

## Steps

```bash
# Initialize repo
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0

# Sync source (first time: 2-4 hours)
repo sync -c -j$(nproc) --force-sync --no-clone-bundle --no-tags

# Download device tree for your device
# Example: OnePlus 9 Pro (lemonadep)
git clone https://github.com/LineageOS/android_device_oneplus_lemonadep -b lineage-21.0 device/oneplus/lemonadep

# Set up environment
. build/envsetup.sh
lunch lineage_lemonadep-user

# Build
mka bacon -j$(nproc)  # output: lineage-21.0-...-SIGNED.zip
```

**Time:** 1-3 hours depending on CPU and if rebuilding from scratch.
