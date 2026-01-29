.PHONY: clean clean-build clean-pyc clean-test clean-docs docs help lint format test servedocs install dev-install build
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

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
	rm -fr site/

lint: ## check style and lint with ruff
	uv run ruff check bbox_visualizer tests examples

format: ## format code with ruff
	uv run ruff format bbox_visualizer tests examples

test: ## run tests with pytest
	uv run pytest

docs: ## build documentation with MkDocs
	mkdocs build --strict

servedocs: ## serve documentation with live reload
	mkdocs serve

build: clean ## build source and wheel package
	uv run python -m build

install: clean ## install the package
	uv pip install .

dev-install: clean ## install in development mode with all extras
	uv pip install -e ".[dev,docs]"
