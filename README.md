# Reticulum MeshChatX

A heavily customized fork of [Reticulum MeshChat](https://github.com/liamcottle/reticulum-meshchat), any meaningful, stable and tested modifications will be submitted as a PR upstream. 

## Features of this fork

- [x] Custom UI/UX (actively being improved)
- [x] Ability to set inbound and propagation node stamps.
- [x] Better config parsing.
- [x] Cancel page fetching or file downloads
- [x] Block recieving messages from users.
- [ ] Spam filter (based on keywords)
- [ ] Multi-identity support.
- [ ] Multi-language support
- [ ] Offline Reticulum documentation tool
- [ ] More tools (translate, LoRa calculator, LXMFy bots, etc)
- [ ] Codebase reorginization and cleanup.
- [ ] Tests and proper CI/CD pipeline.
- [ ] RNS hot reload 
- [ ] Backup/Import identities, messages and interfaces.
- [ ] Full LXST support.
- [ ] Move to Poetry and pyproject.toml for Python packaging.
- [x] More stats on about page.
- [x] Actions are pinned to full-length SHA hashes.
- [x] Docker images are smaller and use SHA256 hashes for the images.
- [x] Electron improvements.
- [x] Latest updates for NPM and Python dependencies (bleeding edge)
- [x] Numerous Ruff, Deepsource, CodeQL Advanced and Bearer Linting/SAST fixes.
- [x] Some performance improvements.

## Usage

Check [releases](https://github.com/Sudo-Ivan/reticulum-meshchatX/releases) for pre-built binaries or appimages.

## Building

```bash
make install
make build
```

### Building in Docker

```bash
make docker-build
```

The build will be in the `dist` directory.

## Development

```bash
make develop
```

## Python packaging

The backend now provides `pyproject.toml` so you can build/install a wheel with `pip install .` or `python -m build`. Before packaging, run `python3 scripts/sync_version.py` (or `make sync-version`) so the generated `src/version.py` reflects the `package.json` version that the Electron artifacts use. The same version helper drives `meshchat.get_app_version()` and `setup.py`, so the CLI release metadata, wheel and AppImage/NSIS bundles stay aligned.

