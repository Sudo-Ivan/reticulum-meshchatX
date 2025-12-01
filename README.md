# Reticulum MeshChatX

A heavily customized fork of [Reticulum MeshChat](https://github.com/liamcottle/reticulum-meshchat), any meaningful, stable and tested modifications will be submitted as a PR upstream. 

## Features of this fork

- [x] Custom UI/UX (actively being improved)
- [x] Ability to set inbound and propagation node stamps
- [x] Better config parsing
- [x] Cancel page fetching or file downloads
- [x] Block recieving messages from users.
- [ ] Spam filter (based on keywords)
- [ ] Multi-identity support
- [x] More stats on about page
- [x] Actions are pinned to full-length SHA hashes.
- [x] Docker images are smaller and use SHA256 hashes for the images.
- [x] Electron improvements
- [x] Latest updates for NPM and Python dependencies (bleeding edge)
- [x] Ruff linting and Bearer SAST fixes

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

