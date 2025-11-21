.PHONY: install run clean

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

install: $(VENV)
	npm install

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) meshchat.py

clean:
	rm -rf $(VENV)
	rm -rf node_modules



