package com.outrageousstorm.romflasher

import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

/**
 * RomFlasher.kt -- Kotlin utility for ROM flashing workflows
 * Compile: kotlinc RomFlasher.kt -include-runtime -d RomFlasher.jar
 * Usage: java -jar RomFlasher.jar --rom <file.zip> --device <model>
 */

data class DeviceInfo(
    val model: String,
    val api: Int,
    val codename: String
)

class RomFlasher(val device: DeviceInfo) {
    fun validateRom(romFile: File): Boolean {
        if (!romFile.exists()) return false
        if (!romFile.name.endsWith(".zip")) return false
        // In real use, would extract and validate structure
        return romFile.length() > 100_000_000 // ROM should be >100MB
    }

    fun createBackup(backupDir: File): String {
        val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"))
        val backupName = "${device.model}_backup_$timestamp"
        backupDir.mkdirs()
        println("📦 Backup location: ${backupDir.absolutePath}/$backupName")
        return backupName
    }

    fun getFlashCommands(romFile: File): List<String> {
        return listOf(
            "adb reboot bootloader",
            "fastboot erase system",
            "fastboot flash system ${romFile.absolutePath}",
            "fastboot -w",  // wipe userdata
            "fastboot reboot"
        )
    }

    fun printFlashGuide(romFile: File) {
        println("\n🚀 ROM Flash Guide for ${device.model}")
        println("═══════════════════════════════════════════")
        println("ROM: ${romFile.name}")
        println("Device: ${device.model} (API ${device.api})")
        println("\nSteps:")
        for ((i, cmd) in getFlashCommands(romFile).withIndex()) {
            println("  ${i+1}. $cmd")
        }
        println("\n⚠️  DO NOT DISCONNECT USB DURING FLASHING")
    }
}

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Usage: java -jar RomFlasher.jar --rom <file.zip> --device <model>")
        return
    }
    
    val romFile = File(args.getOrNull(1) ?: "rom.zip")
    val deviceModel = args.getOrNull(3) ?: "Pixel5"
    
    val device = DeviceInfo(model = deviceModel, api = 31, codename = "redfin")
    val flasher = RomFlasher(device)
    
    if (flasher.validateRom(romFile)) {
        flasher.printFlashGuide(romFile)
    } else {
        println("❌ ROM validation failed")
    }
}
