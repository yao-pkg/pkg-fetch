# Development

This repository contains the scripts and patches used to build and download the Node.js binaries for pkg.

## New releases

Pkg will check for releases of pkg-fetch `<major>.<minor>` version. So each minor/major release of pkg-fetch requires a new GH release with all attached binaries. Patch releases don't require to recreate all new binaries, but only the ones that have changed.

Important things:

- In order to support a new nodejs version we need to create/update the patch in `patches` folder and also `patches/patches.json` file.
- Once the new patch is merged we can trigger the `.github/workflows/build-all.yml` workflow to build all the binaries for all the platforms.
- If this is a minor/major release we need to check the checkbox of the workflow `Upload assets to new draft release`.
- Once the actions will end, copy the sha256 checksums printed at the end of the release body, create a file `shas.txt`, run the command `npm run updateExpected`, that will read the `shas.txt` file and update`lib/expected-shas.json` file with the correct values. Once ended, commit the changes and push them to the repo.
- If this is a minor/major bump, tag and create the official release starting from the draft release created by the workflow.
- If this is not a new release, the `build-all.yml` workflow will copy all asset to the latest release. Remember to update the `expected-shas.json` file with the new checksums anyway.
- Publish `pkg-fetch` to npm.
- Bump `pkg-fetch` version in pkg `package.json` file.
- Release `pkg` to npm.
