// kernel_tuner.rs - Android kernel parameter tuner CLI
// Compiles to single static binary for ADB sideload
use std::process::Command;

fn adb(cmd: &str) -> String {
    let output = Command::new("adb")
        .args(&["shell", cmd])
        .output()
        .expect("failed to run adb");
    String::from_utf8_lossy(&output.stdout).to_string()
}

fn main() {
    println!("🔧 Android Kernel Tuner\n");
    
    let params = vec![
        ("/proc/sys/vm/swappiness", "10"),
        ("/proc/sys/vm/vfs_cache_pressure", "50"),
        ("/proc/sys/kernel/sched_migration_cost_ns", "5000000"),
        ("/proc/sys/kernel/sched_min_granularity_ns", "5000000"),
    ];
    
    for (path, val) in params {
        println!("Setting {} = {}", path, val);
        adb(&format!("echo {} | tee {} >/dev/null", val, path));
    }
    
    println!("\n✅ Kernel tuned for battery life");
}
