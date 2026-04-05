# macOS Build Time Optimization

This document describes the optimizations implemented to improve macOS build times and suggestions for future improvements.

## Problem Statement

macOS x64/arm64 builds were experiencing significant build times:
- Node 20: ~2 hours
- Node 22: ~4 hours  
- Node 24: ~6 hours

These long build times were the main bottleneck in producing new binaries.

## Implemented Optimizations

### 1. Compilation Caching with sccache (Expected: 30-50% improvement on cache hits)

**What:** Added Mozilla's sccache (Shared Compilation Cache) to cache C/C++ compilation results.

**Why:** sccache provides:
- Native GitHub Actions cache integration (`SCCACHE_GHA_ENABLED`)
- Support for concurrent builds without cache conflicts
- Faster than ccache for CI/CD workflows
- Multi-language support (C/C++, Rust)

**Implementation:**
```yaml
- name: Run sccache-cache
  uses: mozilla-actions/sccache-action@v0.0.8

- run: yarn start --node-range node${{ matrix.target-node }} --arch x64 --output dist
  env:
    CC: "sccache clang"
    CXX: "sccache clang++"
```

**Expected Impact:**
- First build: No improvement (cache miss)
- Subsequent builds: 30-50% faster compilation (cache hits)
- Especially effective for patch releases where most code is unchanged

### 2. Optimized Parallel Build Jobs (Expected: 33-50% improvement for arm64)

**What:** Adjusted `MAKE_JOB_COUNT` to match available CPU cores on each runner.

**Why:** 
- Previous: arm64 used only 2 parallel jobs on a 3 vCPU runner (66% utilization)
- Now: arm64 uses 3 parallel jobs (100% utilization)
- x64 already optimal at 4 jobs for 4 vCPU runner

**Changes:**
- **macos-14 (arm64):** Increased from 2 to 3 parallel jobs
- **macos-15-intel (x64):** Kept at 4 parallel jobs

**Expected Impact:**
- arm64: 33-50% faster compilation phase
- x64: No change (already optimal)

### 3. Yarn Dependency Caching (Expected: 30-60 seconds saved per build)

**What:** Added yarn cache to `setup-node` action.

**Why:** Avoids re-downloading and reinstalling node_modules on every build.

**Implementation:**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'yarn'
```

**Expected Impact:**
- Saves 30-60 seconds per build on cache hits

## Overall Expected Improvement

Combining all optimizations:

**First Build (all cache misses):**
- Minimal improvement (~5% from parallel jobs on arm64)

**Subsequent Builds (cache hits):**
- **Best case:** 35-55% reduction in build time
  - Example: Node 24 could go from 6 hours to 2.7-3.9 hours
- **Typical case:** 25-40% reduction
  - Example: Node 24 could go from 6 hours to 3.6-4.5 hours

The actual improvement depends on:
- How much code changed between builds (affects sccache hit rate)
- Network conditions (affects download times)

## Future Optimization Opportunities

### 1. Node.js Source Archive Caching (Potential: 1-2 minutes saved per build)

**What:** Cache downloaded Node.js source tarballs to avoid re-downloading on every build.

**Why:** Each build downloads ~50MB+ source archive from nodejs.org. Caching could eliminate this download time.

**Implementation:**
```yaml
- name: Cache Node.js source archive
  uses: actions/cache@v4
  with:
    path: ~/.pkg-cache/node
    key: node-source-${{ matrix.target-node }}-${{ hashFiles('patches/patches.json') }}
    restore-keys: |
      node-source-${{ matrix.target-node }}-
```

**Considerations:**
- Need to ensure cache invalidation works correctly when patches change
- May interfere with build process if cache is corrupted

### 2. Switch from Full LTO to ThinLTO (Potential: 45-70% faster link times)

**Current State:** Builds use `--enable-lto` (Full Link-Time Optimization)
- Provides best binary performance
- Very slow link phase (can take 30-60+ minutes)

**Proposed:** Switch to ThinLTO (`-flto=thin`)
- 45-70% faster link times compared to Full LTO
- Maintains 95%+ of performance benefits
- Better suited for CI/CD workflows

**Implementation:**
Would require changes to `lib/build.ts`:
```typescript
// In getConfigureArgs function
if (major >= 12) {
  if (hostPlatform !== 'win') {
    // Consider ThinLTO for faster builds
    // args.push('--enable-lto');  // Full LTO
    // Or set via CFLAGS/CXXFLAGS: -flto=thin
  }
}
```

**Risk:** Needs thorough testing to ensure binary quality/performance is maintained.

### 3. Use Larger GitHub Actions Runners (Potential: 2-3x faster)

**Current:** Standard runners (3-4 vCPU)
**Available:** XLarge runners (M2 Pro with 5-core CPU, more RAM)

**Pros:**
- More CPU cores = more parallel compilation
- More RAM = less risk of OOM with higher parallel jobs
- Newer M2 chips = faster per-core performance

**Cons:**
- Significantly higher cost per minute
- Cost/benefit analysis needed

### 4. Distributed Compilation with distcc/sccache remote backend

**What:** Distribute compilation across multiple machines

**Pros:**
- Can dramatically reduce build times for large rebuilds
- sccache already supports S3/GCS remote backends

**Cons:**
- Complex setup
- Requires remote cache infrastructure
- May not be cost-effective for GitHub Actions

### 5. Optimize configure/build flags

**Potential areas:**
- Skip unnecessary build steps for pkg binaries
- Optimize compiler flags for build speed vs runtime performance
- Consider skipping tests during build (already done)

## Monitoring Build Times

To track the effectiveness of these optimizations:

1. Monitor workflow run times in GitHub Actions
2. Compare build times before and after optimizations
3. Track cache hit rates in workflow logs (sccache prints statistics)
4. Look for the sccache stats at the end of builds:
   ```
   sccache stats:
   Compile requests: XXX
   Cache hits: XXX (XX%)
   ```

## References

- [sccache documentation](https://github.com/mozilla/sccache)
- [GitHub Actions caching best practices](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [ThinLTO vs Full LTO comparison](https://clang.llvm.org/docs/ThinLTO.html)
- [Node.js build optimization discussion](https://github.com/nodejs/build/issues/4053)
