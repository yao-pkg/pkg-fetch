# Development

This repository contains the scripts and patches used to build and download the Node.js binaries for pkg.

## New releases

Pkg will check for releases of pkg-fetch `<major>.<minor>` version. So each minor/major release of pkg-fetch requires a new GH release with all attached binaries. Patch releases don't require to recreate all new binaries, but only the ones that have changed.

Important things:

- In order to support a new nodejs version we need to create/update the patch in `patches` folder and also `patches/patches.json` file.
- Our CI workflow will test the new patch to see if it applies cleanly. If so we also suggest to run pkg-fetch locally with `-t` (`--test`) flag to test the patch. It will use `lib/verify.ts` script to verify that the patch is working correctly (this will take some time as it will download nodejs, apply the patch, compile it and run the test).
- Once the new patch is merged we can trigger the `.github/workflows/build-all.yml` workflow to build all the binaries for all the platforms.
- If this is a minor/major release we need to check the checkbox of the workflow `Upload assets to new draft release`.
- Once the actions will end, copy the sha256 checksums printed at the end of the release body, create a file `shas.txt`, run the command `npm run updateExpected`, that will read the `shas.txt` file and update`lib/expected-shas.json` file with the correct values. Once ended, commit the changes and push them to the repo.
- If this is a **minor/major** bump, tag and create the official release starting from the draft release created by the workflow. N.B: **The new release tag must be in the format `v<major>.<minor>`. If different pkg will not be able to download the binaries.**
- If this is a **patch** release, the `build-all.yml` workflow will attach all new asset to the latest release and add new sha hash at the end of the release body. Remember to update the `expected-shas.json` file with the new checksums, copy also the previous checksum and keep only latest version foreach node major (ex: if the previous had node 18.15.0 now keep only hash for 18.18.2).
- Publish `pkg-fetch` to npm with `npm run release` command. This will create the git tag and publish to npm.
- Bump `pkg-fetch` version in `pkg` `package.json` file.
- Release `pkg` to npm with `npm run release` command. This will create the git tag, publish pkg to npm and publish a release with changelog.
