#!/usr/bin/env node
"""
rom_info.js -- Extract and display ROM metadata from ZIP file
Usage: node rom_info.js rom.zip
Shows: build version, security patch, device model, features
"""
const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

function analyzeROM(romPath) {
    try {
        const zip = new AdmZip(romPath);
        const entries = zip.getEntries();
        
        const info = {
            filename: path.basename(romPath),
            filesize: (fs.statSync(romPath).size / 1024 / 1024).toFixed(2) + ' MB',
            files: entries.length,
            hasMeta: entries.some(e => e.entryName.includes('META-INF')),
            hasSystem: entries.some(e => e.entryName.includes('system.img') || e.entryName.includes('system/')),
            hasVendor: entries.some(e => e.entryName.includes('vendor')),
            hasBoot: entries.some(e => e.entryName.includes('boot.img')),
            hasRecovery: entries.some(e => e.entryName.includes('recovery')),
        };
        
        // Try to find build.prop equivalent
        const buildEntry = entries.find(e => 
            e.entryName.includes('build.prop') && 
            !e.isDirectory
        );
        
        if (buildEntry) {
            const buildProp = buildEntry.getData().toString();
            const lines = buildProp.split('\n');
            info.buildProps = {};
            lines.forEach(line => {
                const match = line.match(/^([^=]+)=(.+)$/);
                if (match) {
                    const key = match[1];
                    const val = match[2];
                    if (key.includes('version') || key.includes('patch') || key.includes('device') || key.includes('fingerprint')) {
                        info.buildProps[key] = val;
                    }
                }
            });
        }
        
        console.log('\n🔍 ROM Info');
        console.log('═'.repeat(50));
        console.log(`File: ${info.filename}`);
        console.log(`Size: ${info.filesize}`);
        console.log(`Total files: ${info.files}`);
        console.log('\nPartitions:');
        console.log(`  ${info.hasSystem ? '✓' : '✗'} system`);
        console.log(`  ${info.hasVendor ? '✓' : '✗'} vendor`);
        console.log(`  ${info.hasBoot ? '✓' : '✗'} boot`);
        console.log(`  ${info.hasRecovery ? '✓' : '✗'} recovery`);
        console.log(`  ${info.hasMeta ? '✓' : '✗'} metadata`);
        
        if (info.buildProps) {
            console.log('\nBuild properties:');
            Object.entries(info.buildProps).forEach(([k, v]) => {
                console.log(`  ${k.split('.').pop()}: ${v}`);
            });
        }
        
    } catch (err) {
        console.error('✗ Error reading ROM:', err.message);
    }
}

const romPath = process.argv[2];
if (!romPath) {
    console.log('Usage: node rom_info.js <rom.zip>');
    process.exit(1);
}

analyzeROM(romPath);
