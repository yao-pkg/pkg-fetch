import fetch from 'node-fetch';
import crypto from 'crypto';
import { createReadStream, createWriteStream, mkdirSync, renameSync, rmSync } from 'fs';
import { chmod, stat } from 'fs/promises';
import httpsProxyAgent from 'https-proxy-agent';
import path from 'path';
import { spawnSync, SpawnSyncOptions } from 'child_process';
import stream from 'stream';

import { coerce } from 'semver';
import { log, wasReported } from './log';

export async function downloadUrl(url: string, file: string): Promise<void> {
  log.enableProgress(path.basename(file));
  log.showProgress(0);

  const proxy =
    process.env.HTTPS_PROXY ??
    process.env.https_proxy ??
    process.env.HTTP_PROXY ??
    process.env.http_proxy;

  let res;
  try {
    res = await fetch(
      url,
      proxy ? { agent: httpsProxyAgent(proxy) } : undefined
    );
  } catch (err) {
    log.disableProgress();
    throw wasReported(`Network error during fetch: ${(err as Error).message}`);
  }

  if (!res.ok) {
    log.disableProgress();
    throw wasReported(`${res.status}: ${res.statusText}`);
  }

  const tempFile = `${file}.downloading`;
  mkdirSync(path.dirname(tempFile), { recursive: true });
  const ws = createWriteStream(tempFile);

  const totalSize = Number(res.headers.get('content-length'));
  let currentSize = 0;

  res.body.on('data', (chunk: Buffer) => {
    if (totalSize != null && totalSize !== 0) {
      currentSize += chunk.length;
      log.showProgress((currentSize / totalSize) * 100);
    }
  });
  res.body.pipe(ws);

  return new Promise<void>((resolve, reject) => {
    stream.finished(ws, (err) => {
      if (err) {
        log.disableProgress();
        rmSync(tempFile);
        reject(wasReported(`${err.name}: ${err.message}`));
      } else {
        log.showProgress(100);
        log.disableProgress();
        renameSync(tempFile, file);
        resolve();
      }
    });
  });
}

export async function hash(filePath: string): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    const resultHash = crypto.createHash('sha256');
    const input = createReadStream(filePath);

    input.on('error', (e) => {
      reject(e);
    });

    input.on('readable', () => {
      const data = input.read();
      if (data) {
        resultHash.update(data);
      } else {
        resolve(resultHash.digest('hex'));
      }
    });
  });
}

export async function plusx(file: string) {
  const s = await stat(file);
  const newMode = s.mode | 64 | 8 | 1;
  if (s.mode === newMode) return;
  const base8 = newMode.toString(8).slice(-3);
  await chmod(file, base8);
}

export async function spawn(
  command: string,
  args?: ReadonlyArray<string>,
  options?: SpawnSyncOptions
): Promise<void> {
  const { error } = spawnSync(command, args, options);
  if (error) {
    throw error;
  }
}

export function nodeBinarySortFunction(a: string, b: string): number {
  const coercedVersionA = coerce(a);
  const coercedVersionB = coerce(b);
  if (coercedVersionA && coercedVersionB) {
    return coercedVersionA.compare(coercedVersionB);
  }
  return 0;
}
