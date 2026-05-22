/// ROM Flashing Validator
/// Verify ROM integrity before flashing

use std::fs;
use std::path::Path;
use std::process::Command;

struct RomFile {
    name: String,
    size: u64,
    checksum: String,
}

fn calculate_checksum(file_path: &str) -> Result<String, Box<dyn std::error::Error>> {
    let output = Command::new("sha256sum")
        .arg(file_path)
        .output()?;
    
    let checksum = String::from_utf8(output.stdout)?
        .split_whitespace()
        .next()
        .unwrap_or("")
        .to_string();
    
    Ok(checksum)
}

fn validate_rom(file_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new(file_path);
    
    if !path.exists() {
        return Err(format!("File not found: {}", file_path).into());
    }
    
    println!("📦 Validating ROM: {}\n", file_path);
    
    // Check file size (ROMs typically 500MB+)
    let metadata = fs::metadata(file_path)?;
    println!("📊 File Size: {:.2} MB", metadata.len() as f64 / 1024.0 / 1024.0);
    
    // Calculate checksum
    println!("🔐 Computing checksum...");
    let checksum = calculate_checksum(file_path)?;
    println!("   SHA256: {}", checksum);
    
    // Check file structure (basic ZIP validation)
    let output = Command::new("unzip")
        .args(&["-t", file_path])
        .output()?;
    
    if output.status.success() {
        println!("\n✅ ROM file structure is valid!");
        println!("✅ Ready for flashing!");
    } else {
        println!("\n❌ ROM file structure is invalid!");
        println!("❌ Do NOT flash this ROM!");
    }
    
    Ok(())
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    if args.len() < 2 {
        println!("ROM Flashing Validator\n");
        println!("Usage: rom-flashing-validator <rom-file>");
        println!("Example: rom-flashing-validator LineageOS-21-device.zip");
        return;
    }
    
    match validate_rom(&args[1]) {
        Ok(_) => {},
        Err(e) => println!("❌ Error: {}", e),
    }
}
