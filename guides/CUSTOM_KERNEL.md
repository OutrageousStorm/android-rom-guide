# Custom Kernel Compilation

Build your own Android kernel with performance and battery optimizations.

## Prerequisites

```bash
# Install build tools
sudo apt install build-essential bc bison flex libelf-dev libssl-dev

# Download kernel source (example: AOSP kernel)
git clone https://android.googlesource.com/kernel/msm
cd msm
git checkout android13-stable
```

## Setup build environment

```bash
# Set architecture (ARM64)
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export CROSS_COMPILE_ARM32=arm-linux-gnu-

# Install cross-compiler
sudo apt install gcc-aarch64-linux-gnu gcc-arm-linux-gnueabihf
```

## Configure kernel

```bash
# Get device defconfig (from device or ROM)
adb pull /proc/config.gz
gunzip config.gz
mv config .config

# Or use a defconfig from AOSP
cp arch/arm64/configs/msm8916_defconfig .config

# Customize (menuconfig is optional)
make menuconfig
```

## Build

```bash
# Build kernel image
make -j$(nproc) Image

# Build device tree
make -j$(nproc) dtbs

# Build modules (if used)
make -j$(nproc) modules
INSTALL_MOD_PATH=./output make modules_install
```

## Output

```bash
# Compiled kernel
ls -lh arch/arm64/boot/Image*

# Device trees
ls -lh arch/arm64/boot/dts/*/

# Modules (optional)
ls -lh output/lib/modules/
```

## Flash to device

```bash
# Pack into boot image with ramdisk
adb shell make_ext4fs -s -L system output/boot.img
adb flash boot arch/arm64/boot/Image

# Or via recovery (TWRP)
adb reboot recovery
# In TWRP: Install > select your kernel.zip
```

## Performance optimizations

### Disable unnecessary features
```bash
# In menuconfig, disable:
# - Crypto (CONFIG_CRYPTO) if not needed
# - SELinux (CONFIG_SECURITY_SELINUX) — removes enforcing overhead
# - AIO (CONFIG_AIO) — async I/O overhead
# - DEBUG options — much slower
```

### Enable performance features
```bash
# Enable in .config:
CONFIG_HAS_MMAP=y
CONFIG_HAVE_EFFICIENT_UNALIGNED_ACCESS=y
CONFIG_INLINE_SPIN_LOCKS=y
```

## Common issues

| Issue | Fix |
|-------|-----|
| Build fails: arm64-linux-gnu-gcc not found | `sudo apt install gcc-aarch64-linux-gnu` |
| Device won't boot after flash | Revert to original kernel; check defconfig is correct |
| Modules won't load | Ensure kernel version matches module build |

---

**Time estimate:** 30–60 minutes (depending on CPU cores).

Next: explore KernelSU for rootless kernel modifications.
