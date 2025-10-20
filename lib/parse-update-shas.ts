import * as fs from 'fs';
import * as path from 'path';
import { log, wasReported } from './log';

function parseAndUpdateShas(inputFile: string): void {
  // Read the input file containing new SHAs
  if (!fs.existsSync(inputFile)) {
    throw wasReported(`Input file ${inputFile} does not exist`);
  }

  const input = fs.readFileSync(inputFile, 'utf8');
  const lines = input.split('\n').map(l => l.trim()).filter(Boolean);

  // Read existing shas.txt
  const shasPath = path.join(process.cwd(), 'shas.txt');
  let shasTxt = '';
  try {
    shasTxt = fs.readFileSync(shasPath, 'utf8');
  } catch (e) {
    log.info('shas.txt not found, creating new one');
    shasTxt = '';
  }

  let shasArr = shasTxt.split('\n');

  // Process each line from input
  for (const line of lines) {
    const [sha, patchName] = line.split(/\s+/);
    if (!sha || !patchName) {
      log.warn(`Skipping invalid line: ${line}`);
      continue;
    }

    // Extract major, os, arch. E.g.: node-v22.20.0-win-x64
    const match = patchName.match(/^node-v(\d+)\.[^ ]*-(.+)-(.+)$/);
    if (!match) {
      log.warn(`Skipping line with invalid patch name format: ${line}`);
      continue;
    }

    const major = match[1];
    const os = match[2];
    const arch = match[3];

    // Regex for matching line in shas.txt
    const re = new RegExp(`^\\S+\\s+node-v${major}\\.([0-9.]+){2}-${os}-${arch}$`);
    let found = false;

    shasArr = shasArr.map(l => {
      if (re.test(l)) {
        found = true;
        log.info(`Updating: ${l} -> ${sha}  ${patchName}`);
        return `${sha}  ${patchName}`;
      }
      return l;
    });

    if (!found) {
      log.info(`Adding new entry: ${sha}  ${patchName}`);
      shasArr.push(`${sha}  ${patchName}`);
    }
  }

  // Write updated shas.txt
  const filteredShas = shasArr.filter(Boolean);
  const updatedContent = filteredShas.length > 0 ? `${filteredShas.join('\n')}\n` : '';
  fs.writeFileSync(shasPath, updatedContent);
  log.info(`Successfully updated ${shasPath}`);
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    log.error('Usage: parse-update-shas.ts <input-file>');
    log.error('  input-file: Path to file containing SHA lines in format "<sha> <patch-name>"');
    process.exit(1);
  }

  const inputFile = args[0];
  try {
    parseAndUpdateShas(inputFile);
  } catch (error) {
    if (error instanceof Error && !('wasReported' in error)) {
      log.error(error);
    }
    process.exit(1);
  }
}

export { parseAndUpdateShas };