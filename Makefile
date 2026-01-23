# Makefile for rawget

.PHONY: help venv install build clean test publish test-publish release test-install

BIN := venv/bin
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
PRINTF_FORMAT := "  %-25s %s\n"
PYTEST := $(BIN)/pytest

help:
	@printf $(PRINTF_FORMAT) "help" "Show this help message"
	@printf $(PRINTF_FORMAT) "venv" "Create a virtual environment"
	@printf $(PRINTF_FORMAT) "install" "Install the package in editable mode with dev dependencies"
	@printf $(PRINTF_FORMAT) "build" "Build the package"
	@printf $(PRINTF_FORMAT) "clean" "Clean up build artifacts"
	@printf $(PRINTF_FORMAT) "test" "Run tests"
	@printf $(PRINTF_FORMAT) "publish" "Publish the package to PyPI"
	@printf $(PRINTF_FORMAT) "test-publish" "Publish the package to TestPyPI"
	@printf $(PRINTF_FORMAT) "release" "Clean, build, and publish the package"
	@printf $(PRINTF_FORMAT) "test-install" "Install the package from TestPyPI"

venv:
	@test -d venv || python3 -m venv venv
	@$(PYTHON) -m pip install --upgrade pip

install: venv
	@$(PIP) install -e ".[dev]"

build:
	@$(PYTHON) -m build

clean:
	@rm -rf venv
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name "*.pyc" -exec rm -f {} +
	@find . -name "*.egg-info" -exec rm -rf {} +
	rm -rf dist

test:
	@$(PYTEST)

publish: build test
	@$(PYTHON) -m twine upload dist/*

test-publish: build test
	@$(PYTHON) -m twine upload --repository testpypi dist/*

release: clean install build test publish

test-install: venv
	@$(PIP) install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ rawget
