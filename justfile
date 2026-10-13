# Task runner: https://github.com/casey/just
# Requires: `uv`, `npm`, and `just`.

# List all the justfile recipes.
help:
    just --list --list-prefix 'just '

# Remove all the Python cache files.
clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +

# Install the dependencies, the Playwright browser, and the git hooks.
install: clean-pyc
    uv sync --dev
    npm ci
    uv run playwright install chromium
    uv run prek install

# Lint the server code with uv.
lint-server:
    uv run ruff format --check .
    uv run ruff check .
    SKIP=ruff-check,ruff-format,lint-css,lint-format uv run prek run --all-files

# Lint the client code with Prettier and Stylelint.
lint-client:
    npm run lint --loglevel silent

# Run all linters.
lint: lint-server lint-client

# Format the server code with uv.
format-server:
    uv run ruff check . --fix
    uv run ruff format .
    SKIP=ruff-check,ruff-format,lint-css,lint-format uv run prek run --all-files

# Format the client code with Prettier.
format-client:
    npm run format

# Run all formatters.
format: format-server format-client

# Run tests with pytest.
test:
    uv run pytest

test-lowest-deps:
    #!/usr/bin/env bash
    set -euo pipefail
    lowest_python=$(uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml","rb"))["project"]["requires-python"].removeprefix(">=").strip())')
    uv run --isolated --python "$lowest_python" --resolution lowest-direct playwright install chromium
    uv run --isolated --python "$lowest_python" --resolution lowest-direct pytest

test-highest-deps:
    uv run --isolated --with 'Django, Wagtail' pytest

# Run tests with coverage.
coverage:
    uv run pytest --cov src/wagtail_non_admin_draftail
    uv run coverage report -m
    uv run coverage html

# Compile the SCSS sources into the shipped draftail.css.
build-css:
    npm run build:css

# Extract messages for translation.
makemessages *args:
    @# Pass any additional arguments to the `makemessages` command, e.g. `just makemessages -l=es`.
    @# default to `--all` if no arguments are provided.
    cd src/wagtail_non_admin_draftail && uv run ../../testmanage.py makemessages --ignore="test/*" {{ if args != "" { args } else { "--all" } }}

# Compile translation message catalogs for use.
compilemessages:
    cd src/wagtail_non_admin_draftail && uv run ../../testmanage.py compilemessages
