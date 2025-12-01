# Reticulum MeshChatX

A heavily customized fork of [Reticulum MeshChat](https://github.com/liamcottle/reticulum-meshchat), any meaningful, stable and tested modifications will be submitted as a PR upstream. 

## Features of this fork

- [x] Custom UI/UX (actively being improved)
- [x] Ability to set inbound and propagation node stamps.
- [x] Better config parsing.
- [x] Cancel page fetching or file downloads
- [x] Block receiving messages from users.
- [ ] Spam filter (based on keywords)
- [ ] Multi-identity support.
- [ ] Multi-language support
- [ ] Offline Reticulum documentation tool
- [ ] More tools (translate, LoRa calculator, LXMFy bots, etc.)
- [x] Codebase reorganization and cleanup.
- [ ] Tests and proper CI/CD pipeline.
- [ ] RNS hot reload 
- [ ] Backup/Import identities, messages and interfaces.
- [ ] Full LXST support.
- [x] Poetry for packaging and dependency management.
- [x] More stats on about page.
- [x] Actions are pinned to full-length SHA hashes.
- [x] Docker images are smaller and use SHA256 hashes for the images.
- [x] Electron improvements (ASAR and security).
- [x] Latest updates for NPM and Python dependencies (bleeding edge)
- [x] Numerous Ruff, Deepsource, CodeQL Advanced and Bearer Linting/SAST fixes.
- [x] Some performance improvements.

## Usage

Check [releases](https://github.com/Sudo-Ivan/reticulum-meshchatX/releases) for pre-built binaries or appimages.

## Building

```bash
make install   # installs Python deps via Poetry and Node deps via npm
make build
```

You can run `make run` or `make develop` (a thin alias) to start the backend + frontend loop locally through `poetry run meshchat`.

### Python packaging

The Python build is driven entirely by Poetry now. Run `python scripts/sync_version.py` or `make sync-version` before packaging so `pyproject.toml` and `src/version.py` match `package.json`. After that:

```bash
python -m poetry install
make wheel  # produces a wheel in python-dist/ that bundles the public assets
```

The wheel includes the frontend `public/` assets, `logo/`, and the CLI entry point, and `python-dist/` keeps the artifact separate from the Electron `dist/` output.

### Building in Docker

```bash
make build-docker
```

`build-docker` creates `reticulum-meshchatx:local` (or `$(DOCKER_IMAGE)` if you override it) via `docker buildx`. Set `DOCKER_PLATFORMS` to `linux/amd64,linux/arm64` when you need multi-arch images, and adjust `DOCKER_BUILD_FLAGS`/`DOCKER_BUILD_ARGS` to control `--load`/`--push`.

### Running with Docker Compose

```bash
make run-docker
```

`run-docker` feeds the locally-built image into `docker compose -f docker-compose.yml up --remove-orphans --pull never reticulum-meshchatx`. The compose file uses the `MESHCHAT_IMAGE` env var so you can override the target image without editing the YAML (the default still points at `ghcr.io/sudo-ivan/reticulum-meshchatx:latest`). Use `docker compose down` or `Ctrl+C` to stop the container.

The Electron build artifacts will still live under `dist/` for releases.

## Python packaging

The backend uses Poetry with `pyproject.toml` for dependency management and packaging. Before building, run `python3 scripts/sync_version.py` (or `make sync-version`) to ensure the generated `src/version.py` reflects the version from `package.json` that the Electron artifacts use. This keeps the CLI release metadata, wheel packages, and other bundles aligned.

### Building with Poetry

```bash
# Install dependencies
poetry install

# Build the package
poetry build

# Install locally for testing
pip install dist/*.whl
```

### Building with pip (alternative)

If you prefer pip, you can build/install directly:

```bash
# Build the wheel
pip install build
python -m build

# Install locally
pip install .
```

### cx_Freeze (for AppImage/NSIS)

The `cx_setup.py` script uses cx_Freeze for creating standalone executables (AppImage for Linux, NSIS for Windows). This is separate from the Poetry/pip packaging workflow.

