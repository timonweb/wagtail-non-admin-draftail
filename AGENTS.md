# Agents

Important context for AI coding agents working on this project.

## Project overview

Non-admin Draftail is a Django/Wagtail package that lets Wagtail's Draftail rich-text editor run on regular (non-admin) Django form
pages, including the link, image, document and embed modals. The source code is in `src/wagtail_non_admin_draftail/`, with tests in
`tests/` and a demo site in `demo/`.

This project follows the layout of the [cookiecutter-wagtail-package](https://github.com/wagtail/cookiecutter-wagtail-package)
template and the [Wagtail package maintenance guidelines](https://wagtail.org/package-guidelines/).

## Key commands

```sh
just help              # View all commands
just install           # Install Python and Node.js dependencies, the Playwright browser and git hooks
just demo              # Run the demo site (migrate + runserver)
just test              # Run tests with pytest (includes Playwright end-to-end tests)
just test-lowest-deps  # Run tests against the lowest supported Python, Django and Wagtail
just lint              # Run all linters (Ruff, prek, Prettier, Stylelint)
just format            # Run all formatters (Ruff, Prettier)
just coverage          # Run tests with coverage report
just build-css         # Compile static_src SCSS into the shipped draftail.css
just makemessages      # Extract messages for translation
just compilemessages   # Compile translation message catalogs for use
```

The demo has its own Django tests: `uv run ./demo/manage.py test notes`.

## Quality assurance

- Python: Ruff for linting and formatting (`ruff.toml`), prek hooks (`prek.toml`).
- JavaScript/CSS/JSON/YAML: Prettier for formatting (`prettier.config.js`).
- CSS: Stylelint with `@wagtail/stylelint-config-wagtail` (`stylelint.config.mjs`).
- Tests: pytest with pytest-django and pytest-playwright. Test settings are in `src/wagtail_non_admin_draftail/test/settings.py`.
- CI: GitHub Actions in `.github/workflows/`.

Always run `just lint` and `just test` before considering work complete.

## Project layout

```
src/wagtail_non_admin_draftail/             # Package source code
src/wagtail_non_admin_draftail/static_src/  # SCSS sources for draftail.css (not shipped)
src/wagtail_non_admin_draftail/test/        # Django test app with settings, URLs (not shipped)
tests/                                      # Test modules (pytest); test_e2e_*.py use Playwright
demo/                                       # Demo site with a notes app
.github/workflows/                          # CI: linting, tests, scheduled Wagtail release tests, publishing
```

## Guidelines

- All package views require a logged-in user, and uploads go to the public-uploads collection. Keep that access model when adding views.
- Pages using the editor need both `wagtail_non_admin_draftail/draftail_media.html` and `{{ form.media }}`.
- The compiled `draftail.css` is committed; rebuild it with `just build-css` after SCSS changes.
- Follow [Semantic Versioning](https://semver.org/) for releases.
- Use [Keep a Changelog](https://keepachangelog.com/) format for CHANGELOG.md.
- Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.
