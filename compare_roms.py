#!/usr/bin/env python3
"""compare_roms.py - Compare Android ROMs by features, performance, and security"""
import json, argparse

ROMS = {
    'LineageOS': {'base': 'AOSP', 'bloatware': 'minimal', 'privacy': 'good', 'customization': 'excellent', 'gapps': 'optional'},
    'GrapheneOS': {'base': 'AOSP', 'bloatware': 'none', 'privacy': 'maximum', 'customization': 'limited', 'gapps': 'no'},
    'CalyxOS': {'base': 'AOSP', 'bloatware': 'minimal', 'privacy': 'excellent', 'customization': 'good', 'gapps': 'optional'},
    'CrDroid': {'base': 'LineageOS', 'bloatware': 'minimal', 'privacy': 'good', 'customization': 'excellent', 'gapps': 'optional'},
    'Evolution X': {'base': 'AOSP', 'bloatware': 'minimal', 'privacy': 'good', 'customization': 'excellent', 'gapps': 'bundled'},
}

def compare(args):
    selected = [r for r in ROMS if not args.filter or args.filter.lower() in r.lower()]
    if args.json:
        print(json.dumps({r: ROMS[r] for r in selected}, indent=2))
        return
    print("\n🔍 ROM Comparison\n")
    cols = ['Bloatware', 'Privacy', 'Customization', 'GApps']
    print(f"{'ROM':<20}", end='')
    for c in cols: print(f"{c:<15}", end='')
    print()
    print('─' * 80)
    for rom in selected:
        info = ROMS[rom]
        print(f"{rom:<20}", end='')
        for col in cols:
            key = col.lower().replace(' ', '')
            val = info.get(col.lower().replace(' ', ''), '?')
            print(f"{val:<15}", end='')
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filter', help='Filter ROMs by name')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    compare(args)
