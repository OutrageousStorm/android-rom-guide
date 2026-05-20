#!/usr/bin/env python3
"""
compare_roms.py — Compare Android ROMs by features, performance, security
Usage: python3 compare_roms.py
       python3 compare_roms.py --csv output.csv
"""
import json, csv, argparse

ROMS = [
    {'name': 'LineageOS 21', 'base': 'Android 14', 'bloat': 'minimal', 'root': '✅ Magisk', 
     'features': ['Google apps optional', 'Full customization', 'Active support'],
     'perf': '⭐⭐⭐⭐', 'security': '⭐⭐⭐', 'privacy': '⭐⭐⭐⭐'},
    {'name': 'TWRP Custom', 'base': 'Varies', 'bloat': 'none', 'root': '✅ KernelSU',
     'features': ['Ultra customizable', 'AOSP only', 'Community ROMs'],
     'perf': '⭐⭐⭐⭐⭐', 'security': '⭐⭐', 'privacy': '⭐⭐⭐⭐⭐'},
    {'name': 'GrapheneOS', 'base': 'Android 14', 'bloat': 'none', 'root': '❌ Hardened kernel',
     'features': ['Privacy-first', 'Sandboxed Google Play', 'No bloat'],
     'perf': '⭐⭐⭐⭐', 'security': '⭐⭐⭐⭐⭐', 'privacy': '⭐⭐⭐⭐⭐'},
    {'name': 'CalyxOS', 'base': 'Android 14', 'bloat': 'minimal', 'root': '❌ No root',
     'features': ['DuckDuckGo integration', 'Seedvault backups', 'Datura firewall'],
     'perf': '⭐⭐⭐⭐', 'security': '⭐⭐⭐⭐⭐', 'privacy': '⭐⭐⭐⭐'},
    {'name': 'DivestOS', 'base': 'Android 14', 'bloat': 'none', 'root': '✅ Optional',
     'features': ['Hardened F-Droid', 'Minimal patches', 'Libre firmware'],
     'perf': '⭐⭐⭐⭐', 'security': '⭐⭐⭐⭐', 'privacy': '⭐⭐⭐⭐⭐'},
]

def print_table():
    print("\n📊 Android ROM Comparison\n")
    print(f"{'ROM':<20} {'Base':<12} {'Bloat':<10} {'Root':<18} {'Performance':<8} {'Security':<8} {'Privacy':<8}")
    print("─" * 95)
    for rom in ROMS:
        print(f"{rom['name']:<20} {rom['base']:<12} {rom['bloat']:<10} {rom['root']:<18} {rom['perf']:<8} {rom['security']:<8} {rom['privacy']:<8}")
    
    print("\n🎯 Best for...\n")
    print("  Custom ROMs:         TWRP Custom (maximum performance & customization)")
    print("  Privacy-First:       GrapheneOS (sandboxed, hardened, no Google)")
    print("  Balanced:            LineageOS 21 (feature-complete, stable, rooted)")
    print("  Minimal Overhead:    CalyxOS (lightweight, useful integrations)")
    print("  Hardened & Libre:    DivestOS (minimal patches, libre firmware)
")

def export_csv(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ROM', 'Base', 'Bloat', 'Root', 'Performance', 'Security', 'Privacy', 'Features'])
        for rom in ROMS:
            writer.writerow([
                rom['name'], rom['base'], rom['bloat'], rom['root'],
                rom['perf'], rom['security'], rom['privacy'],
                ' | '.join(rom['features'])
            ])
    print(f"✅ Exported to {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='Export to CSV')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()
    
    if args.json:
        print(json.dumps(ROMS, indent=2))
    elif args.csv:
        export_csv(args.csv)
    else:
        print_table()
