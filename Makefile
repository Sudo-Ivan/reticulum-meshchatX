.PHONY: install run develop clean build build-appimage build-exe dist sync-version wheel node_modules python build-docker run-docker

PYTHON ?= python
POETRY = $(PYTHON) -m poetry
NPM = npm

DOCKER_COMPOSE_CMD ?= docker compose
DOCKER_COMPOSE_FILE ?= docker-compose.yml
DOCKER_IMAGE ?= reticulum-meshchatx:local
DOCKER_BUILDER ?= meshchatx-builder
DOCKER_PLATFORMS ?= linux/amd64
DOCKER_BUILD_FLAGS ?= --load
DOCKER_BUILD_ARGS ?=
DOCKER_CONTEXT ?= .
DOCKERFILE ?= Dockerfile

install: sync-version node_modules python

node_modules:
	$(NPM) install

python:
	$(POETRY) install

run: install
	$(POETRY) run meshchat

develop: run

build: install
	$(NPM) run build

wheel: install
	$(POETRY) build -f wheel
	$(PYTHON) scripts/move_wheels.py

build-appimage: build
	$(NPM) run electron-postinstall
	$(NPM) run dist -- --linux AppImage

build-exe: build
	$(NPM) run electron-postinstall
	$(NPM) run dist -- --win portable

dist: build-appimage

clean:
	rm -rf node_modules
	rm -rf build
	rm -rf dist
	rm -rf python-dist
	rm -rf meshchatx/public

sync-version:
	$(PYTHON) scripts/sync_version.py

build-docker:
	@if ! docker buildx inspect $(DOCKER_BUILDER) >/dev/null 2>&1; then \
		docker buildx create --name $(DOCKER_BUILDER) --use >/dev/null; \
	else \
		docker buildx use $(DOCKER_BUILDER); \
	fi
	docker buildx build --builder $(DOCKER_BUILDER) --platform $(DOCKER_PLATFORMS) \
		$(DOCKER_BUILD_FLAGS) \
		-t $(DOCKER_IMAGE) \
		$(DOCKER_BUILD_ARGS) \
		-f $(DOCKERFILE) \
		$(DOCKER_CONTEXT)

run-docker:
	MESHCHAT_IMAGE="$(DOCKER_IMAGE)" \
		$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) up --remove-orphans --pull never reticulum-meshchatx
