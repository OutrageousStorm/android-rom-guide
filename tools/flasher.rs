fn main() {
    println!("🔥 ROM Flasher");
    println!("==============\n");

    // Check device
    let output = std::process::Command::new("adb")
        .arg("devices")
        .output()
        .expect("Failed to run adb");

    let devices = String::from_utf8_lossy(&output.stdout);
    if !devices.contains("device") {
        eprintln!("❌ No device connected");
        return;
    }

    println!("✓ Device connected");
    println!("Ready to flash ROM");
}
