.PHONY: install run develop clean build build-appimage build-exe dist sync-version wheel node_modules python

PYTHON ?= python
POETRY = $(PYTHON) -m poetry
NPM = npm

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

sync-version:
	$(PYTHON) scripts/sync_version.py
