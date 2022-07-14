SHELL := /bin/bash

ifndef VERBOSE
.SILENT:
endif

.PHONY: create-venv install clean-build clean-test


ifdef VIRTUAL_ENV
VENV_DIR = $(VIRTUAL_ENV)
else ifdef venv
VENV_DIR = $(venv)
else
VENV_DIR = ./.venv
endif

PIP = $(VENV_DIR)/bin/pip
PYTHON = $(VENV_DIR)/bin/python
PIP_COMPILE = $(VENV_DIR)/bin/pip-compile
PYTEST = $(VENV_DIR)/bin/pytest


clean: clean-build clean-test

clean-build:
	rm -rf dist/
	rm -rf .eggs/
	rm -rf adg.egg-info/

clean-test:
	rm -rf htmlcov/
	rm -f adg_logstash.log
	rm -f .coverage
	rm -f coverage.xml
	rm -f nose2-junit.xml

create-venv:
	test -d $(VENV_DIR) || python3.9 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel pip-tools

install: create-venv
	$(PIP) install -r requirements.txt

requirements: create-venv
	$(PIP_COMPILE) -v --upgrade requirements.in