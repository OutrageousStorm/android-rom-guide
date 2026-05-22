import Denoopts from "https://deno.land/std@0.208.0/flags/mod.ts";

interface ROM {
  name: string;
  baseAndroid: string;
  lastUpdate: string;
  customizations: string[];
  bloat: string;
  stability: string;
}

const ROMs: Record<string, ROM> = {
  lineageos: {
    name: "LineageOS",
    baseAndroid: "14+",
    lastUpdate: "May 2026",
    customizations: ["System-wide themes", "Navbar customization", "Privacy Guard"],
    bloat: "Minimal",
    stability: "Excellent"
  },
  crDroid: {
    name: "crDroid",
    baseAndroid: "14+",
    lastUpdate: "May 2026",
    customizations: ["Lots of tweaks", "UI customization", "Performance options"],
    bloat: "Minimal",
    stability: "Very Good"
  },
  pixelExperience: {
    name: "Pixel Experience",
    baseAndroid: "14+",
    lastUpdate: "May 2026",
    customizations: ["Pixel UI", "Stock Android feel", "Clean design"],
    bloat: "Very Low",
    stability: "Excellent"
  },
  aospExtended: {
    name: "AOSP Extended",
    baseAndroid: "14+",
    lastUpdate: "May 2026",
    customizations: ["Advanced customization", "Gestures", "System tweaks"],
    bloat: "Low",
    stability: "Good"
  }
};

function compareROMs(rom1: string, rom2: string) {
  const r1 = ROMs[rom1];
  const r2 = ROMs[rom2];
  
  if (!r1 || !r2) {
    console.log("ROM not found. Available ROMs:", Object.keys(ROMs).join(", "));
    return;
  }
  
  console.log(`\n📱 Comparing: ${r1.name} vs ${r2.name}\n`);
  console.log(`Base Android:     ${r1.baseAndroid}        vs  ${r2.baseAndroid}`);
  console.log(`Last Update:      ${r1.lastUpdate}     vs  ${r2.lastUpdate}`);
  console.log(`Bloat Level:      ${r1.bloat}         vs  ${r2.bloat}`);
  console.log(`Stability:        ${r1.stability}     vs  ${r2.stability}`);
  console.log(`\nCustomizations:`);
  console.log(`  ${r1.name}: ${r1.customizations.join(", ")}`);
  console.log(`  ${r2.name}: ${r2.customizations.join(", ")}`);
}

function listROMs() {
  console.log("\nAvailable ROMs:\n");
  Object.entries(ROMs).forEach(([key, rom]) => {
    console.log(`  ${key.padEnd(15)} → ${rom.name} (Android ${rom.baseAndroid})`);
  });
}

const args = Denoopts.parse(Deno.args);

if (args.list) {
  listROMs();
} else if (args._.length >= 2) {
  compareROMs(args._[0] as string, args._[1] as string);
} else {
  console.log("ROM Comparison CLI\n");
  console.log("Usage:");
  console.log("  deno run rom-compare.ts <rom1> <rom2>  - Compare two ROMs");
  console.log("  deno run rom-compare.ts --list         - List all ROMs\n");
  listROMs();
}
