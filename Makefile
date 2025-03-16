.PHONY: clean clean-test clean-pyc clean-build clean-docs docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-docs: ## remove documentation build artifacts
	rm -fr docs/_build/
	rm -f docs/bbox_visualizer.rst
	rm -f docs/modules.rst

lint: ## check style and lint with ruff
	uv run ruff check bbox_visualizer tests examples

format: ## format code with ruff
	uv run ruff format bbox_visualizer tests examples

test: ## run tests with pytest
	uv pip install pytest
	uv run pytest

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/bbox_visualizer.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ bbox_visualizer
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

build: clean ## builds source and wheel package
	uv pip install build
	uv run python -m build

release: build ## package and upload a release
	uv pip install twine
	uv run python -m twine check dist/*
	uv run python -m twine upload dist/*

install: clean ## install the package to the active Python's site-packages
	uv pip install .

dev-install: clean ## install the package in development mode with all extras
	uv pip install -e ".[dev]"

bump-version: ## Bump version in both files (Usage: make bump-version NEW_VERSION=0.2.1)
	@if [ "$(NEW_VERSION)" = "" ]; then \
		echo "Please provide NEW_VERSION (e.g. make bump-version NEW_VERSION=0.2.1)"; \
		exit 1; \
	fi
	sed -i '' 's/version = "[0-9.]*"/version = "$(NEW_VERSION)"/' pyproject.toml
	sed -i '' 's/__version__ = "[0-9.]*"/__version__ = "$(NEW_VERSION)"/' bbox_visualizer/_version.py
	git add pyproject.toml bbox_visualizer/_version.py
	git commit -m "Bump version to $(NEW_VERSION)"
	git tag v$(NEW_VERSION)
	git push origin v$(NEW_VERSION)
	git push origin
