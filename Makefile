# Makefile for Copley Escalators Server app.
#
# This Makefile assumes that you have "virtualenv" and "pip" installed
# globally.
#
# The "devel" and "prod" recipes will set up a local virtualenv in
# "./.venv", which is a location compatible with most of the
# virtualenvwrapper and helper tools (notably, the oh-my-zsh
# virtualenvwrapper plugin).

.PHONY: devel prod test serve
.SUFFIXES:

prod: .venv/prod
devel: .venv/devel

.venv/devel: .venv requirements/devel.txt
	source .venv/bin/activate; \
	pip install -Ur requirements/devel.txt
	touch requirements/devel.txt
	touch .venv/devel

.venv/prod: .venv requirements/prod.txt
	source .venv/bin/activate; \
	pip install -Ur requirements/prod.txt
	touch requirements/prod.txt
	touch .venv/prod

.venv:
	test -d .venv || virtualenv .venv
	.venv/bin/pip install --upgrade pip

serve: devel
	source .venv/bin/activate; \
	FLASK_CONFIG="copleyescalators.settings.local.LocalConfig" \
	FLASK_DEBUG=1 \
	FLASK_APP=server.py \
	flask run --host=0.0.0.0

test: devel
	source .venv/bin/activate; \
	FLASK_CONFIG="copleyescalators.settings.testing.TestingConfig" \
	python -m unittest discover
