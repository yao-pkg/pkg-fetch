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
