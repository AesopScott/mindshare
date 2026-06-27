const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const releaseDir = path.join(root, 'release');
const blockedNamePatterns = [
  /^\.env($|\.)/i,
  /\.pem$/i,
  /\.pfx$/i,
  /\.key$/i,
  /\.log$/i,
  /chrome-extension\.crx$/i,
  /extension-update\.xml$/i
];
const blockedPathPatterns = [
  /[\\/]\.git([\\/]|$)/i,
  /[\\/]graphify-out([\\/]|$)/i,
  /[\\/]chrome-extension([\\/]|$)/i,
  /[\\/]native-host([\\/]|$)/i
];

function walk(dir, found = []) {
  if (!fs.existsSync(dir)) return found;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath, found);
    } else {
      found.push(fullPath);
    }
  }
  return found;
}

const files = walk(releaseDir);
const blocked = files.filter((file) => {
  const relative = path.relative(releaseDir, file);
  const base = path.basename(file);
  return blockedNamePatterns.some((pattern) => pattern.test(base)) ||
    blockedPathPatterns.some((pattern) => pattern.test(relative));
});

if (!fs.existsSync(releaseDir)) {
  console.error(`Release directory not found: ${releaseDir}`);
  process.exit(1);
}

if (blocked.length) {
  console.error('Package verification failed. Blocked files found:');
  for (const file of blocked) {
    console.error(`- ${path.relative(releaseDir, file)}`);
  }
  process.exit(1);
}

const installers = files
  .filter((file) => /\.(exe|msi|zip)$/i.test(file))
  .map((file) => path.relative(releaseDir, file));

if (!installers.length) {
  console.error('Package verification failed. No installer, portable EXE, MSI, or ZIP was found.');
  process.exit(1);
}

console.log('Package verification passed.');
console.log(`Artifacts: ${installers.join(', ')}`);
