# ROM Flasher

Fast C-based ROM flashing utility for Android devices via ADB.

## Build

```bash
make
# or
gcc -o rom-flasher rom-flasher.c
```

## Usage

```bash
# Basic flash
./rom-flasher lineageos-34.zip

# With data wipe
./rom-flasher lineageos-34.zip --wipe

# Using sideload mode
./rom-flasher lineageos-34.zip --sideload
```

## Features
- ZIP validation
- ADB integration
- Sideload support
- Wipe option
- Fast C implementation
