# 🔧 Android Kernel Compilation Guide

Build a custom kernel from source for your device.

## Prerequisites

```bash
# Ubuntu/Debian
sudo apt install build-essential python3 libssl-dev bison flex bc

# Mac
brew install binutils libssl coreutils findutils gnu-sed

# Get device kernel source
# https://github.com/android-kernel (official)
# https://github.com/YOUR_BRAND/kernel_YOUR_DEVICE (OEM specific)
```

## Quick Start

```bash
git clone https://github.com/android-kernel/kernel_oneplus_sm8350.git
cd kernel_*
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-

# Get a prebuilt toolchain
git clone https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9

# Copy device config
cp arch/arm64/configs/gki_defconfig .config

# Compile
make -j$(nproc)
```

## Output
- `arch/arm64/boot/Image.gz` — compressed kernel
- `arch/arm64/boot/dts/qcom/sm8350-oneplus.dtb` — device tree

## Flashing

```bash
# Boot into TWRP recovery with boot.img
adb reboot recovery

# Push kernel
adb push arch/arm64/boot/Image.gz /tmp/

# Flash via recovery flashable zip or direct
```

## Customization

Edit `.config` to:
- Enable/disable modules
- Adjust CPU governors, I/O schedulers
- Tweak thermal thresholds
- Custom build strings

Common tweaks:
```bash
# Menuconfig
make menuconfig
# Navigate: Device Drivers → ...

# CPU frequency scaling
CONFIG_CPUFREQ_DT=y
CONFIG_CPUFREQ_POWERSAVE=y

# I/O scheduler
CONFIG_IOSCHED_CFQ=y
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Compilation error | Ensure correct toolchain for your kernel version |
| Boot loop | Check kernel serial, match to device |
| No modules | `make modules && make modules_install` |

