import { fetch, ProxyAgent } from 'undici';
import crypto from 'crypto';
import { createReadStream, createWriteStream, mkdirSync, renameSync, rmSync } from 'fs';
import { chmod, stat } from 'fs/promises';
import path from 'path';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';
import { spawnSync, SpawnSyncOptions } from 'child_process';

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
      proxy ? { dispatcher: new ProxyAgent(proxy) } : undefined
    );
  } catch (err) {
    log.disableProgress();
    throw wasReported(`Network error during fetch: ${(err as Error).message}`);
  }

  if (!res.ok || !res.body) {
    log.disableProgress();
    throw wasReported(`${res.status}: ${res.statusText}`);
  }

  const tempFile = `${file}.downloading`;
  mkdirSync(path.dirname(tempFile), { recursive: true });
  const ws = createWriteStream(tempFile);

  const totalSize = Number(res.headers.get('content-length'));
  let currentSize = 0;

  const body = Readable.fromWeb(res.body);
  body.on('data', (chunk: Buffer) => {
    if (totalSize != null && totalSize !== 0) {
      currentSize += chunk.length;
      log.showProgress((currentSize / totalSize) * 100);
    }
  });

  // `pipeline` propagates errors from the source (`body`) as well as the
  // destination (`ws`), so a truncated/aborted download rejects loudly instead
  // of leaving the promise unsettled and the process exiting silently.
  try {
    await pipeline(body, ws);
  } catch (err) {
    log.disableProgress();
    rmSync(tempFile, { force: true });
    throw wasReported(`${(err as Error).name}: ${(err as Error).message}`);
  }

  log.showProgress(100);
  log.disableProgress();
  renameSync(tempFile, file);
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
