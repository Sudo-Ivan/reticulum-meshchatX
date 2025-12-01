.PHONY: install run clean build build-appimage build-exe dist

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
NPM = npm

install: $(VENV) node_modules

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

node_modules:
	$(NPM) install

run: install
	$(PYTHON) meshchat.py

build: install
	$(NPM) run build

build-appimage: build
	$(NPM) run electron-postinstall
	$(NPM) run dist -- --linux AppImage

build-exe: build
	$(NPM) run electron-postinstall
	$(NPM) run dist -- --win portable

dist: build-appimage

clean:
	rm -rf $(VENV)
	rm -rf node_modules
	rm -rf build
	rm -rf dist



