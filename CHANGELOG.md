## [3.5.14](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.13...v3.5.14) (2024-10-01)

### Bug Fixes

- node 22 module filename resolution in win32 ([#49](https://github.com/yao-pkg/pkg-fetch/issues/49)) by [@faulpeltz](https://github.com/faulpeltz) ([e436d74](https://github.com/yao-pkg/pkg-fetch/commit/e436d74e4cdfdd8cd4004b672c9d0c3d0e78abc0))
- skip sha check when providing `PKG_NODE_PATH` ([#50](https://github.com/yao-pkg/pkg-fetch/issues/50)) ([76bc9d0](https://github.com/yao-pkg/pkg-fetch/commit/76bc9d0bbf77d03d4505bad289b2b640b7e5f40f))

### Chores

- add release workflow ([d1b15b3](https://github.com/yao-pkg/pkg-fetch/commit/d1b15b3f0f6f1a90ccb4c08c8f9f75ecd675250d))

## [3.5.13](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.12...v3.5.13) (2024-09-20)

### Features

- add v22.9.0 patch ([#47](https://github.com/yao-pkg/pkg-fetch/issues/47)) ([588dda6](https://github.com/yao-pkg/pkg-fetch/commit/588dda6744fc4416da753a235a502f58789c1570))

### Bug Fixes

- automatically trigger shas update workflow when building new patches ([721dac7](https://github.com/yao-pkg/pkg-fetch/commit/721dac7aba6199fc4aee2ebef162b91209916964))
- update expected shas ([01f2951](https://github.com/yao-pkg/pkg-fetch/commit/01f295148440e13f733d8b576821c9bcfa34bc11))

### Chores

- add missing sed target ([7a53cce](https://github.com/yao-pkg/pkg-fetch/commit/7a53ccee9ead7fe44b8706e47134223f641e3efe))
- change default `upload assets` to false ([cab8e80](https://github.com/yao-pkg/pkg-fetch/commit/cab8e805caf22daf0647331cea5a307e6b710371))
- create update expected workflow ([0a5f961](https://github.com/yao-pkg/pkg-fetch/commit/0a5f9611a2ba22659f85251eae14a96585e9e441))
- create workflow to automatically check new nodejs releases ([effe040](https://github.com/yao-pkg/pkg-fetch/commit/effe040902bbe51d555361c103893aba1173a194))
- fix regex ([ce4d0f8](https://github.com/yao-pkg/pkg-fetch/commit/ce4d0f879795cbce095aef32124033145a77523b))
- handle case where patch major doesn't exists ([fba9824](https://github.com/yao-pkg/pkg-fetch/commit/fba982472abffcdb99afafc5f5f05051ba377821))
- restore `if` statement ([1a87466](https://github.com/yao-pkg/pkg-fetch/commit/1a87466d8ba574a83051024560a72f070f002dba))
- restore working version ([385375d](https://github.com/yao-pkg/pkg-fetch/commit/385375d4873f7e0d0cb9f5f6826b2234bc713fc6))
- test run ([7400fc9](https://github.com/yao-pkg/pkg-fetch/commit/7400fc9568ed37dc31407f01936010ac47291b4b))
- try different approach ([267990e](https://github.com/yao-pkg/pkg-fetch/commit/267990e69b8c2da1c99143ff72b73501e7789ddf))

## [3.5.12](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.11...v3.5.12) (2024-09-17)

### Bug Fixes

- switch to macos-14 runner and cleanup before build ([#46](https://github.com/yao-pkg/pkg-fetch/issues/46)) ([75d4ca0](https://github.com/yao-pkg/pkg-fetch/commit/75d4ca09c874b3c8785a966b8f5ba235c3c9fcd8))
- update expected shas ([75e67b8](https://github.com/yao-pkg/pkg-fetch/commit/75e67b8214327dd0a24cf4c4bea8c93ddfd254b7))

### Chores

- add patch/minor release scripts to package.json ([9c57a56](https://github.com/yao-pkg/pkg-fetch/commit/9c57a567c55566d22b2aac281d0e51cda9000dfe))

## [3.5.11](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.10...v3.5.11) (2024-09-10)

### Features

- add Node 22 patch ([#45](https://github.com/yao-pkg/pkg-fetch/issues/45)) (by [@faulpeltz](https://github.com/faulpeltz)) ([1703cd2](https://github.com/yao-pkg/pkg-fetch/commit/1703cd2f284455c4316a44496537915f532ebd29))

### Bug Fixes

- update expected shas ([bc5d8a5](https://github.com/yao-pkg/pkg-fetch/commit/bc5d8a545c4f8b09718754bd6f8cc5c9902b9e15))

## [3.5.10](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.9...v3.5.10) (2024-09-06)

### Features

- add v18.20.2 patch ([#35](https://github.com/yao-pkg/pkg-fetch/issues/35)) ([36e3726](https://github.com/yao-pkg/pkg-fetch/commit/36e37262893aa1a698a150d0e6f235cec972f41e))
- add v18.20.4 patch ([#43](https://github.com/yao-pkg/pkg-fetch/issues/43)) ([2a45bc5](https://github.com/yao-pkg/pkg-fetch/commit/2a45bc5b3db6bcf37bf136175008eebaa23bf781))
- add v20.12.1 patch ([#32](https://github.com/yao-pkg/pkg-fetch/issues/32)) ([9cb16d3](https://github.com/yao-pkg/pkg-fetch/commit/9cb16d361670b5bd5dfff6db27a20b003095f996))
- node 20.14.0 ([#37](https://github.com/yao-pkg/pkg-fetch/issues/37)) ([f35e749](https://github.com/yao-pkg/pkg-fetch/commit/f35e749bcaff95d1262d6303fdfba564f32383be))
- node 20.17.0 ([#44](https://github.com/yao-pkg/pkg-fetch/issues/44)) ([480ebec](https://github.com/yao-pkg/pkg-fetch/commit/480ebec19a69dc1d30dff01a880b206f8a7b68ef))

### Bug Fixes

- macos nodejs 18 build ([81e4e1b](https://github.com/yao-pkg/pkg-fetch/commit/81e4e1b6d68df3ce08049871b0b4134f1e028c91))
- nodejs 18 patch `sys/random.h` not included ([1defa22](https://github.com/yao-pkg/pkg-fetch/commit/1defa22a8b1f5b70fa78cb870a09a69337b78621))
- revert v20.12.1 patch ([#32](https://github.com/yao-pkg/pkg-fetch/issues/32)) ([f673feb](https://github.com/yao-pkg/pkg-fetch/commit/f673feb48bff7c5b7e8fd733337e09cebb369e31))
- update shas ([9d496d0](https://github.com/yao-pkg/pkg-fetch/commit/9d496d0eb888283ddc722244315d116e5af80f3d))
- use macos-13/14 runner ([#40](https://github.com/yao-pkg/pkg-fetch/issues/40)) ([f79b7a3](https://github.com/yao-pkg/pkg-fetch/commit/f79b7a3585146d5228734bc405cf3d1a0b744a34))

### Chores

- add test patch workflow ([2e14897](https://github.com/yao-pkg/pkg-fetch/commit/2e148971aa9f0c951097646548c53f898e209bfb))
- correct package name ([5caf157](https://github.com/yao-pkg/pkg-fetch/commit/5caf157a9ea33383da8df8af4818b23afd0a3f4a))
- remove shas.txt from ignore ([94482c7](https://github.com/yao-pkg/pkg-fetch/commit/94482c7c3a8d90f540a5ed3e39afb6e138955c9b))

## [3.5.9](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.8...v3.5.9) (2024-02-16)

### Features

- add v18.19.1 patch ([#28](https://github.com/yao-pkg/pkg-fetch/issues/28)) ([3845065](https://github.com/yao-pkg/pkg-fetch/commit/3845065386ba99dc30ff731f2f9a6d49b210e50f))
- add v20.11.1 patch ([#29](https://github.com/yao-pkg/pkg-fetch/issues/29)) ([a69918b](https://github.com/yao-pkg/pkg-fetch/commit/a69918b166b5b32be4e74cff96b7be066d87988d))

### Bug Fixes

- bump expected-shas.json ([d58bdcb](https://github.com/yao-pkg/pkg-fetch/commit/d58bdcb96cdc293ca77ce73a1340e63918429b51))

### Chores

- fix patch node workflow ([#24](https://github.com/yao-pkg/pkg-fetch/issues/24)) ([34c5ab3](https://github.com/yao-pkg/pkg-fetch/commit/34c5ab30bb0e35ca1190dbe1749cb39918a6f829))
- make workflow update patches.json ([361fd63](https://github.com/yao-pkg/pkg-fetch/commit/361fd63e7193ee42ff9d51f9228e47db5bc03c9d))
- patch node workflow ([0f00204](https://github.com/yao-pkg/pkg-fetch/commit/0f0020420ea60924fd1f05af64ae215c37396930))

## [3.5.8](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.7...v3.5.8) (2024-02-06)

### Features

- drop node 19 ([a4fa899](https://github.com/yao-pkg/pkg-fetch/commit/a4fa8992a08bb2c597ac6222063a6f023f6fc07e))
- node 20.11.0 and 18.19.0 patches ([#18](https://github.com/yao-pkg/pkg-fetch/issues/18)) ([de81e9f](https://github.com/yao-pkg/pkg-fetch/commit/de81e9f50c7e5c6c796762503cef8c3dc66fbffe))

### Bug Fixes

- add missing binaries shas ([16392db](https://github.com/yao-pkg/pkg-fetch/commit/16392dbfc1f0a9b559c323c9986f84f646b9113f))
- build issues ([#20](https://github.com/yao-pkg/pkg-fetch/issues/20)) ([59a2c69](https://github.com/yao-pkg/pkg-fetch/commit/59a2c69e8d8d544a5711ab0fe09a08ba9d040327))
- bump shas ([#21](https://github.com/yao-pkg/pkg-fetch/issues/21)) ([7099e0f](https://github.com/yao-pkg/pkg-fetch/commit/7099e0f006f025cc89a0004f85f04841be9541d6))
- mac-os uploaded artifacts ([#23](https://github.com/yao-pkg/pkg-fetch/issues/23)) ([7b7e2ce](https://github.com/yao-pkg/pkg-fetch/commit/7b7e2ce56ecbf923fe843958ad9ff160389a69ea))
- patches for arm64 ([#15](https://github.com/yao-pkg/pkg-fetch/issues/15)) ([c7dff09](https://github.com/yao-pkg/pkg-fetch/commit/c7dff099190a393a27f24880b154dbc87acb2ede))
- windows build ([#22](https://github.com/yao-pkg/pkg-fetch/issues/22)) ([65a09c7](https://github.com/yao-pkg/pkg-fetch/commit/65a09c7458cdf33c399e4c0f0628e015495ce39e))

### Chores

- bump actions ([#19](https://github.com/yao-pkg/pkg-fetch/issues/19)) ([3f7d742](https://github.com/yao-pkg/pkg-fetch/commit/3f7d742305cd83badc9ea03dbba517c8fad23ba4))
- remove all calls to "set-output" from actions ([#14](https://github.com/yao-pkg/pkg-fetch/issues/14)) ([1461d59](https://github.com/yao-pkg/pkg-fetch/commit/1461d596fac6e86334694ef4440ea1d966380e67))

### Documentation

- update docs ([2eb79e5](https://github.com/yao-pkg/pkg-fetch/commit/2eb79e529f4f9574030afd4cc2e7c505b38bdc52))

## [3.5.7](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.6...v3.5.7) (2023-12-05)

### Features

- support for latest NodeJS v20 ([#11](https://github.com/yao-pkg/pkg-fetch/issues/11)) ([31bbc32](https://github.com/yao-pkg/pkg-fetch/commit/31bbc321666278877749d6023d259cd0ab50675a))

### Bug Fixes

- node20 patch syntax error winx64 ([2ba1dd8](https://github.com/yao-pkg/pkg-fetch/commit/2ba1dd8939764330e0f373ce38efc68d6e890ed9)), closes [#11](https://github.com/yao-pkg/pkg-fetch/issues/11)
- update expected shas ([98624e3](https://github.com/yao-pkg/pkg-fetch/commit/98624e3a522401962b496dc6e682c75d986b4e1d))
- update expected shas ([fc07c46](https://github.com/yao-pkg/pkg-fetch/commit/fc07c4659546849a57de06cdf91599cb9f7c9c6b))
- v20 patch ARM64 ([#12](https://github.com/yao-pkg/pkg-fetch/issues/12)) ([07ed56d](https://github.com/yao-pkg/pkg-fetch/commit/07ed56d3e3b45f233b3ef4e92d3458c4eb32e1d9))

### Chores

- add .yarn to gitignore ([729c0a1](https://github.com/yao-pkg/pkg-fetch/commit/729c0a1871a7d70843cbc5ad9fd70c08c4c2757d))
- add missing macos-linux v20 matrix ([28d96e9](https://github.com/yao-pkg/pkg-fetch/commit/28d96e99af719107d3ee4211d987a6f0e8dd9800))
- update vscode settings ([a787d4d](https://github.com/yao-pkg/pkg-fetch/commit/a787d4d7bb071419394d917f94677bfc6249c720))

## [3.5.6](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.5...v3.5.6) (2023-10-28)

### Features

- macOS arm64 build ([#8](https://github.com/yao-pkg/pkg-fetch/issues/8)) ([8f8986f](https://github.com/yao-pkg/pkg-fetch/commit/8f8986f0daea763e1ec0b2d3238f5acfd77b0f28))

### Bug Fixes

- update expected sha ([82cddb0](https://github.com/yao-pkg/pkg-fetch/commit/82cddb03df6723fccb2102efa68ea4e6c232ae97))

## [3.5.5](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.4...v3.5.5) (2023-10-17)

### Features

- support for custom `PKG_NODE_PATH` ([#7](https://github.com/yao-pkg/pkg-fetch/issues/7)) ([4bfcccb](https://github.com/yao-pkg/pkg-fetch/commit/4bfcccb9af1b600cb47509d8eef90efe9d2c84c7))

### Bug Fixes

- update expected sha of node 18.18.2 and 16.20.2 ([#6](https://github.com/yao-pkg/pkg-fetch/issues/6)) ([62ffff2](https://github.com/yao-pkg/pkg-fetch/commit/62ffff231b2f12b886c4d420f999d238fce4c655))
- update to node 18.18.2 and node 16.20.2 ([#4](https://github.com/yao-pkg/pkg-fetch/issues/4)) ([7a62329](https://github.com/yao-pkg/pkg-fetch/commit/7a6232968d8431f162052d60ba23140a1ed761a0))

### Chores

- add `--ignore-engines` to all install comands ([6c9ac01](https://github.com/yao-pkg/pkg-fetch/commit/6c9ac01407e36fa6bdcdb0376e481bd97f392778))

### Documentation

- add important notice about new releases ([66457a2](https://github.com/yao-pkg/pkg-fetch/commit/66457a27f85d2fe8563f7b86b36ee7bfd41ba28a))

## [3.5.4](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.3...v3.5.4) (2023-10-04)

### Bug Fixes

- update expected shas ([056e749](https://github.com/yao-pkg/pkg-fetch/commit/056e7497a4e46162101d36428977a48c09cfe10b))

## [3.5.3](https://github.com/yao-pkg/pkg-fetch/compare/v3.5.2...v3.5.3) (2023-10-04)

### Bug Fixes

- change repo name and fetch url ([dba6017](https://github.com/yao-pkg/pkg-fetch/commit/dba60177fd822a413df0ba32d952e4773d9c6603))

### Chores

- add release script ([#3](https://github.com/yao-pkg/pkg-fetch/issues/3)) ([bd1ccb6](https://github.com/yao-pkg/pkg-fetch/commit/bd1ccb659b6e6281f6343f5c21b86d686a077bcd))
- do not create gh release ([3c2c1ba](https://github.com/yao-pkg/pkg-fetch/commit/3c2c1baab883c590429170e4d51cd1a376e8f785))
- fix lock and editor ([#2](https://github.com/yao-pkg/pkg-fetch/issues/2)) ([dff791d](https://github.com/yao-pkg/pkg-fetch/commit/dff791d7819ec32d9c1ff90023ab385c6dcc946b))
- fix package.json name ([4026ce8](https://github.com/yao-pkg/pkg-fetch/commit/4026ce8ed526ecb6f10b04f31d558fe18e4b3a93))
- npm error fix ([8212e14](https://github.com/yao-pkg/pkg-fetch/commit/8212e14d70346930f033240001b2ba02a53eaeb8))

### Documentation

- add development docs ([#1](https://github.com/yao-pkg/pkg-fetch/issues/1)) ([cc7de4b](https://github.com/yao-pkg/pkg-fetch/commit/cc7de4bd54ea474be70aa66dd332a0fdd198abf1))
