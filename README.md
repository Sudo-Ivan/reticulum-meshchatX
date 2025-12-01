# Reticulum MeshChatX

A heavily customized fork of [Reticulum MeshChat](https://github.com/liamcottle/reticulum-meshchat)

## Features of this fork

- [x] Custom UI/UX (actively being improved)
- [ ] Ability to set stamps
- [x] Better config parsing
- [x] Cancel page fetching or file downloads
- [ ] Block users
- [ ] Spam filter (based onkeywords)
- [ ] Multi-identity support
- [x] More stats on about page
- [x] Actions are pinned to full-length SHA hashes.
- [x] Docker images are smaller and use SHA256 hashes for the images.

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

