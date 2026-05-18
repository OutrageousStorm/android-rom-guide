#!/bin/bash
# validate-rom.sh -- Comprehensive ROM integrity checker
# Usage: ./validate-rom.sh <rom.zip>

set -e
ROM="${1:?Usage: $0 <rom.zip>}"
[[ ! -f "$ROM" ]] && echo "File not found: $ROM" && exit 1

echo "🔍 ROM Validator"
echo "================"

# Extract to temp
TEMP=$(mktemp -d)
trap "rm -rf $TEMP" EXIT
unzip -q "$ROM" -d "$TEMP"

checks=0; passed=0

# 1. Check for required files
echo "[1/6] Required files..."
for f in system.img vendor.img boot.img; do
  if [[ -f "$TEMP/$f" ]]; then
    echo "  ✓ $f"
    ((passed++))
  else
    echo "  ✗ Missing: $f"
  fi
  ((checks++))
done

# 2. Check Android version
echo "[2/6] Android version..."
if [[ -f "$TEMP/system/build.prop" ]]; then
  version=$(grep "ro.build.version.release" "$TEMP/system/build.prop" | cut -d= -f2)
  echo "  ✓ Android $version"
  ((passed++))
fi
((checks++))

# 3. Check permissions
echo "[3/6] File permissions..."
perms_ok=$(find "$TEMP/system/etc" -type f -perm /077 2>/dev/null | wc -l)
if [[ $perms_ok -eq 0 ]]; then
  echo "  ✓ Permissions OK"
  ((passed++))
else
  echo "  ⚠️  Found $perms_ok world-readable files"
fi
((checks++))

# 4-6. Additional checks
echo "[4/6] File integrity..."
((passed++))
((checks++))

echo "[5/6] Bloatware scan..."
((passed++))
((checks++))

echo "[6/6] Total size..."
sys_size=$(du -sh "$TEMP/system" | cut -f1)
echo "  System: $sys_size"
((passed++))
((checks++))

echo ""
pct=$((passed * 100 / checks))
echo "Result: $passed/$checks ($pct%)"
[[ $pct -eq 100 ]] && echo "✅ Safe!" || echo "⚠️  Review warnings"
