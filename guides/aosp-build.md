# Building AOSP from Source

Complete guide to building Android Open Source Project locally.

## Prerequisites

```bash
# Linux (Ubuntu 20.04+)
sudo apt install git-core gnupg flex bison gperf build-essential \
  zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 \
  lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev \
  libgl1-mesa-dev libxml2-utils xsltproc unzip python-dev python3-dev

# Repo tool
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH
```

## Sync source
```bash
mkdir ~/aosp && cd ~/aosp
repo init -u https://android.googlesource.com/platform/manifest -b android-13.0.0_r1
repo sync -j4 --force-sync  # takes 2-3 hours, ~150GB
```

## Build
```bash
source build/envsetup.sh
lunch sdk_gphone_x86_64-userdebug
make -j$(nproc)  # 30-60 min depending on CPU
```

Output: `out/target/product/generic_x86_64/system.img`

See also: [android-gsi-guide](../android-gsi-guide), [android-kernel-guide](../android-kernel-guide)
