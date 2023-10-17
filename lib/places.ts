import { major, minor } from 'semver';
import os from 'os';
import path from 'path';

const { PKG_CACHE_PATH } = process.env;
const IGNORE_TAG = Boolean(process.env.PKG_IGNORE_TAG);

export const cachePath =
  PKG_CACHE_PATH || path.join(os.homedir(), '.pkg-cache');

function tagFromVersion(version: string) {
  const mj = major(version);
  const mn = minor(version);

  return `v${mj}.${mn}`;
}

interface PlaceOptions {
  version: string;
  nodeVersion: string;
  platform: string;
  arch: string;
}

interface LocalPlaceOptions extends PlaceOptions {
  from: string;
  output?: string;
}

export function localPlace({
  from,
  output,
  version,
  nodeVersion,
  platform,
  arch,
}: LocalPlaceOptions) {
  let binDir: string;

  if(process.env.PKG_NODE_PATH) {
    return path.resolve(process.env.PKG_NODE_PATH);
  }

  if (output) {
    binDir = path.resolve(output);
  } else {
    binDir = IGNORE_TAG
      ? path.join(cachePath)
      : path.join(cachePath, tagFromVersion(version));
  }

  return path.resolve(
    binDir,
    `${output ? 'node' : from}-${nodeVersion}-${platform}-${arch}`
  );
}

export interface Remote {
  tag: string;
  name: string;
}

export function remotePlace({
  version,
  nodeVersion,
  platform,
  arch,
}: PlaceOptions): Remote {
  return {
    tag: tagFromVersion(version),
    name: `node-${nodeVersion}-${platform}-${arch}`,
  };
}
