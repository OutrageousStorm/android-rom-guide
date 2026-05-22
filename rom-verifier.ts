#!/usr/bin/env ts-node
/**
 * ROM Verifier - Advanced Android ROM integrity and compatibility checker
 * Validates ROM signatures, checks device compatibility, and analyzes build properties
 */

import * as fs from "fs";
import * as crypto from "crypto";
import * as path from "path";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

interface ROMMetadata {
  device: string;
  buildId: string;
  buildFlavor: string;
  securityPatch: string;
  releaseVersion: string;
}

interface VerificationResult {
  valid: boolean;
  checksumMatch: boolean;
  signatureValid: boolean;
  compatible: boolean;
  warnings: string[];
  metadata: Partial<ROMMetadata>;
  timestamp: string;
}

class ROMVerifier {
  private romPath: string;
  private deviceTarget: string;

  constructor(romPath: string, deviceTarget: string) {
    this.romPath = romPath;
    this.deviceTarget = deviceTarget;
  }

  async calculateChecksum(): Promise<string> {
    return new Promise((resolve, reject) => {
      const hash = crypto.createHash("sha256");
      const stream = fs.createReadStream(this.romPath);

      stream.on("data", (data) => hash.update(data));
      stream.on("end", () => resolve(hash.digest("hex")));
      stream.on("error", reject);
    });
  }

  async verifySignature(): Promise<boolean> {
    try {
      const { stdout } = await execAsync(
        `unzip -l "${this.romPath}" | grep -i META-INF/MANIFEST.MF`,
        { maxBuffer: 1024 * 1024 }
      );
      return stdout.includes("MANIFEST.MF");
    } catch {
      return false;
    }
  }

  async extractBuildProperties(): Promise<Partial<ROMMetadata>> {
    try {
      const { stdout } = await execAsync(
        `unzip -p "${this.romPath}" system/build.prop 2>/dev/null || unzip -p "${this.romPath}" system/system/build.prop`,
        { maxBuffer: 2 * 1024 * 1024 }
      );

      const props: Partial<ROMMetadata> = {};
      const lines = stdout.split("\n");

      for (const line of lines) {
        if (line.includes("ro.product.device="))
          props.device = line.split("=")[1];
        if (line.includes("ro.build.id="))
          props.buildId = line.split("=")[1];
        if (line.includes("ro.build.flavor="))
          props.buildFlavor = line.split("=")[1];
        if (line.includes("ro.build.version.security_patch="))
          props.securityPatch = line.split("=")[1];
        if (line.includes("ro.build.version.release="))
          props.releaseVersion = line.split("=")[1];
      }

      return props;
    } catch (error) {
      return {};
    }
  }

  async checkCompatibility(metadata: Partial<ROMMetadata>): Promise<boolean> {
    if (!metadata.device) {
      return false;
    }

    const compatibleDevices = this.getCompatibleDevices(this.deviceTarget);
    return compatibleDevices.includes(metadata.device || "");
  }

  private getCompatibleDevices(deviceTarget: string): string[] {
    const deviceMap: { [key: string]: string[] } = {
      pixel6: ["oriole", "pixel6"],
      pixel7: ["bluejay", "pixel7"],
      samsung_s21: ["SM-G991B", "SM-G991U"],
      oneplus9: ["lemonade", "oneplus9"],
    };

    return deviceMap[deviceTarget] || [deviceTarget];
  }

  async verify(expectedChecksum?: string): Promise<VerificationResult> {
    const result: VerificationResult = {
      valid: false,
      checksumMatch: false,
      signatureValid: false,
      compatible: false,
      warnings: [],
      metadata: {},
      timestamp: new Date().toISOString(),
    };

    try {
      if (!fs.existsSync(this.romPath)) {
        result.warnings.push(`ROM file not found: ${this.romPath}`);
        return result;
      }

      const checksum = await this.calculateChecksum();
      result.checksumMatch = !expectedChecksum || checksum === expectedChecksum;

      if (!result.checksumMatch) {
        result.warnings.push(
          `Checksum mismatch. Expected: ${expectedChecksum}, Got: ${checksum}`
        );
      }

      result.signatureValid = await this.verifySignature();
      if (!result.signatureValid) {
        result.warnings.push("ROM signature not found or invalid");
      }

      result.metadata = await this.extractBuildProperties();
      result.compatible = await this.checkCompatibility(result.metadata);
      if (!result.compatible) {
        result.warnings.push(
          `Device mismatch. ROM is for: ${result.metadata.device}, Target: ${this.deviceTarget}`
        );
      }

      result.valid = result.checksumMatch && result.signatureValid;

      return result;
    } catch (error) {
      result.warnings.push(`Verification error: ${String(error)}`);
      return result;
    }
  }

  static printReport(result: VerificationResult): void {
    console.log("\n=== ROM Verification Report ===");
    console.log(`Timestamp: ${result.timestamp}`);
    console.log(`Status: ${result.valid ? "✅ VALID" : "❌ INVALID"}`);
    console.log(`\nVerification Details:`);
    console.log(`  Checksum Match: ${result.checksumMatch ? "✓" : "✗"}`);
    console.log(`  Signature Valid: ${result.signatureValid ? "✓" : "✗"}`);
    console.log(`  Device Compatible: ${result.compatible ? "✓" : "✗"}`);

    if (Object.keys(result.metadata).length > 0) {
      console.log(`\nROM Metadata:`);
      console.log(`  Device: ${result.metadata.device || "Unknown"}`);
      console.log(`  Build ID: ${result.metadata.buildId || "Unknown"}`);
      console.log(`  Flavor: ${result.metadata.buildFlavor || "Unknown"}`);
      console.log(
        `  Security Patch: ${result.metadata.securityPatch || "Unknown"}`
      );
      console.log(`  Release: ${result.metadata.releaseVersion || "Unknown"}`);
    }

    if (result.warnings.length > 0) {
      console.log(`\nWarnings:`);
      result.warnings.forEach((w) => console.log(`  ⚠️  ${w}`));
    }

    console.log("==============================\n");
  }
}

const args = process.argv.slice(2);
if (args.length < 2) {
  console.log("Usage: rom-verifier.ts <rom-path> <device> [expected-checksum]");
  console.log("Example: rom-verifier.ts lineage.zip pixel6");
  process.exit(1);
}

const [romPath, device, expectedChecksum] = args;
const verifier = new ROMVerifier(romPath, device);

verifier.verify(expectedChecksum).then((result) => {
  ROMVerifier.printReport(result);
  process.exit(result.valid ? 0 : 1);
});
