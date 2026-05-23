#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/**
 * ROM Flasher - Fast ADB ROM flashing utility
 * Compile: gcc -o rom-flasher rom-flasher.c
 * Usage: ./rom-flasher <rom.zip> [--wipe] [--sideload]
 */

typedef struct {
    char rom_path[256];
    int wipe_data;
    int use_sideload;
} FlashOptions;

void print_help() {
    printf("ROM Flasher v1.0 - ADB ROM flashing utility\n");
    printf("Usage: ./rom-flasher <rom.zip> [OPTIONS]\n");
    printf("Options:\n");
    printf("  --wipe       Wipe data partition\n");
    printf("  --sideload   Use adb sideload instead of recovery\n");
}

int verify_rom(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp) {
        printf("❌ ROM file not found: %s\n", path);
        return 0;
    }
    
    // Check ZIP header
    unsigned char header[4];
    if (fread(header, 1, 4, fp) != 4) {
        printf("❌ Invalid ROM file\n");
        fclose(fp);
        return 0;
    }
    
    // ZIP files start with 0x50 0x4B (PK)
    if (header[0] != 0x50 || header[1] != 0x4B) {
        printf("❌ Not a valid ZIP file\n");
        fclose(fp);
        return 0;
    }
    
    printf("✓ ROM file verified\n");
    fclose(fp);
    return 1;
}

int flash_rom(FlashOptions *opts) {
    char cmd[512];
    
    printf("🔄 Starting ROM flash...\n");
    
    if (opts->use_sideload) {
        printf("📱 Using ADB sideload mode\n");
        snprintf(cmd, sizeof(cmd), "adb sideload '%s'", opts->rom_path);
    } else {
        snprintf(cmd, sizeof(cmd), 
            "adb push '%s' /sdcard/ && adb reboot recovery", 
            opts->rom_path);
    }
    
    printf("⏳ Executing: %s\n", cmd);
    int ret = system(cmd);
    
    if (ret == 0) {
        printf("✓ Flash command completed successfully\n");
        return 1;
    } else {
        printf("❌ Flash failed with code %d\n", ret);
        return 0;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_help();
        return 1;
    }
    
    FlashOptions opts = {0};
    strncpy(opts.rom_path, argv[1], sizeof(opts.rom_path) - 1);
    
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--wipe") == 0) opts.wipe_data = 1;
        if (strcmp(argv[i], "--sideload") == 0) opts.use_sideload = 1;
    }
    
    if (!verify_rom(opts.rom_path)) {
        return 1;
    }
    
    if (opts.wipe_data) {
        printf("⚠️  Will wipe data after flashing\n");
    }
    
    if (!flash_rom(&opts)) {
        return 1;
    }
    
    printf("✅ ROM flash process initiated\n");
    return 0;
}
