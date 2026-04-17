# LineageOS Advanced Setup

## Build your own LineageOS

```bash
mkdir ~/lineage && cd ~/lineage
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0
repo sync -j8 --force-sync

source build/envsetup.sh
lunch lineage_<device>-userdebug
make -j$(nproc)
```

Output: `out/target/product/<device>/lineage-*.zip`

## Recovery + Kernel customization

LineageOS includes TWRP by default. To use a custom kernel:

```bash
# After repo sync, replace kernel
cp custom-kernel/Image.gz lineage/kernel/brand/device/Image.gz

# Rebuild
mka target-files-package -j8
```

## Signing with your key

```bash
# Generate signing key (once)
subject='/C=US/ST=State/L=City/O=Org/OU=Unit/CN=LineageOS'
openssl genrsa -out testkey.key 4096
openssl req -new -x509 -key testkey.key -out testkey.crt -days 3650 -subj "$subject"

# Sign ROM
java -jar signapk.jar testcert.x509.pem testkey.pk8   lineage-21.0-signed.zip lineage-21.0-custom.zip
```

## SELinux context (advanced)

If flashing fails with SELinux denial:

```bash
# Check denial
adb shell dmesg | grep "denied\|avc:"

# Audit mode (permissive)
adb shell setenforce 0  # temporary
# Or build with PRODUCT_ENFORCE := false
```

## Performance tuning

Edit `lineage/vendor/build/product/system/common.mk`:

```makefile
PRODUCT_SYSTEM_PROPERTIES +=     ro.config.enable_rcc=true     ro.config.avoid_gfx_accel=true     ro.streaming_vibrator_threshold=0     dalvik.vm.heapsize=512m
```

## Upstream updates

Track official LineageOS patches:

```bash
cd lineage
repo forall -c 'git remote add lineage https://github.com/LineageOS/$REPO_PROJECT.git'
repo forall -c 'git fetch lineage lineage-21.0'
repo forall -c 'git rebase lineage/lineage-21.0'
```
