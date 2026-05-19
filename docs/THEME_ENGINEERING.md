# Android Theme Engineering

Deep dive into Android theming — custom Magisk themes, overlay framework, system UI customization.

## Magisk Theme Format

theme_name/
├── common/               # Applied to all apps
├── system/               # System apps only
└── system_ui/            # SystemUI specific

## Overlays (Android Resource Overlays)

Runtime resource replacement without modifying system:

```bash
adb shell cmd overlay enable com.custom.overlay
adb shell cmd overlay set-priority com.custom.overlay 25
adb shell cmd overlay list
```

## Custom Fonts (via Magisk)

fonts_custom/
├── system/fonts/
│   ├── Roboto-Regular.ttf
│   └── Roboto-Bold.ttf
