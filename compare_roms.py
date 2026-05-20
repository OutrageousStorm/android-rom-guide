#!/usr/bin/env python3
"""Compare ROM features: LineageOS, GrapheneOS, CalyxOS, DivestOS, /e/OS"""
import json

ROMS = {
    'LineageOS': {
        'privacy': 7, 'customization': 9, 'updates': 8, 'devices': 200,
        'root': True, 'gapps': 'optional', 'tracking': 'minimal'
    },
    'GrapheneOS': {
        'privacy': 10, 'customization': 4, 'updates': 10, 'devices': 2,
        'root': False, 'gapps': None, 'tracking': 'hardened'
    },
    'CalyxOS': {
        'privacy': 9, 'customization': 7, 'updates': 8, 'devices': 10,
        'root': False, 'gapps': 'microG', 'tracking': 'minimal'
    },
    'DivestOS': {
        'privacy': 9, 'customization': 8, 'updates': 7, 'devices': 150,
        'root': True, 'gapps': 'optional', 'tracking': 'minimal'
    },
    '/e/OS': {
        'privacy': 8, 'customization': 7, 'updates': 7, 'devices': 40,
        'root': False, 'gapps': None, 'tracking': 'minimal'
    },
}

print("ROM Comparison Matrix\n")
print(f"{'ROM':<15} {'Privacy':<10} {'Customization':<15} {'Updates':<10} {'Devices':<10}")
print("─" * 60)
for rom, props in ROMS.items():
    print(f"{rom:<15} {props['privacy']}/10{'':<5} {props['customization']}/10{'':<8} "
          f"{props['updates']}/10{'':<5} {props['devices']}")
