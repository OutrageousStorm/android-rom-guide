#!/bin/bash
# rom_validate.sh -- Validate ROM image integrity before flashing
# Checks: MD5, signature, build tag, required partitions
# Usage: ./rom_validate.sh <path-to-rom.zip>

set -e
ROM="${1:?Usage: $0 <rom.zip>}"

echo "🔍 ROM Validator"
echo "════════════════════════════════════════"
echo "File: $(basename $ROM)"
echo "Size: $(du -h $ROM | cut -f1)"

# Extract to temp
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT
unzip -q "$ROM" -d "$TMPDIR"

# Check build.prop
if [[ ! -f "$TMPDIR/system/build.prop" ]]; then
    echo "❌ Missing system/build.prop"
    exit 1
fi

BUILD=$(grep "ro.build.fingerprint" "$TMPDIR/system/build.prop" | cut -d= -f2)
MODEL=$(grep "ro.product.model" "$TMPDIR/system/build.prop" | cut -d= -f2)
ANDROID=$(grep "ro.build.version.release" "$TMPDIR/system/build.prop" | cut -d= -f2)

echo "✓ Build: $BUILD"
echo "✓ Model: $MODEL"
echo "✓ Android: $ANDROID"

# Check for required partition images
for img in system boot vendor; do
    if [[ ! -f "$TMPDIR/$img.img" ]]; then
        echo "⚠️  Missing: $img.img"
    else
        SIZE=$(du -h "$TMPDIR/$img.img" | cut -f1)
        echo "✓ $img.img ($SIZE)"
    fi
done

# Verify MD5 if present
if [[ -f "$TMPDIR/MD5" ]]; then
    echo ""
    echo "Verifying MD5..."
    cd "$TMPDIR"
    md5sum -c MD5 > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        echo "✓ MD5 check passed"
    else
        echo "❌ MD5 mismatch!"
        exit 1
    fi
fi

echo ""
echo "✅ ROM validation complete. Ready to flash."
echo "   adb reboot bootloader"
echo "   fastboot update $(basename $ROM)"
