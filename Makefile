.PHONY: clean build publish test lint format

# Package management
clean:
	rm -rf dist/*
	rm -rf build/*
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	uv build

publish: build
	uvx twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Development tasks
install:
	uv pip install -e ".[dev]"

test:
	uv run pytest

lint:
	ruff check .

format:
	ruff check . --fix
	ruff format .
# Install development dependencies
dev-setup:
	uv pip install -r requirements-dev.txt

# Run all checks before publishing
pre-publish: clean lint test build 