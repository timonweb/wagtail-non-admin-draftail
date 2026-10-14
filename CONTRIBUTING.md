# Contributing guidelines

Thank you for your interest in this project! Bug reports, fixes and new features are all welcome. Here's how to get set up.

## Installation

The repo includes a small demo site that you can run while working on the package. First, clone the repo:

```sh
git clone https://github.com/timonweb/wagtail-non-admin-draftail.git
cd wagtail-non-admin-draftail
```

> Requirements: [`uv`](https://github.com/astral-sh/uv), [`just`](https://github.com/casey/just) and Node.js (the version in
> `.node-version`). [`prek`](https://prek.j178.dev/) is installed as a dev dependency.

Install the Python and Node.js dependencies, the Playwright browser used by the end-to-end tests, and the git hooks:

```sh
just install
```

Then set up the demo database, create a user and run the demo:

```sh
just migrate
just createsuperuser
just demo
```

Open <http://127.0.0.1:8000/notes/>. Reading notes is public; to write one, log in with the user you just created (the demo uses the
Wagtail admin login).

## Quality assurance

Here are the available recipes:

```sh
just build-css         # Compile the SCSS sources into the shipped draftail.css.
just clean-pyc         # Remove all the Python cache files.
just compilemessages   # Compile translation message catalogs for use.
just coverage          # Run tests with coverage.
just createsuperuser   # Create a demo user.
just demo              # Run the demo application (migrate + runserver).
just demo-gif          # Record docs/demo.gif, the editor demo in the README (needs ffmpeg).
just format            # Run all formatters.
just format-client     # Format the client code with Prettier.
just format-server     # Format the server code with Ruff.
just help              # List all the justfile recipes.
just install           # Install the dependencies, the Playwright browser, and the git hooks.
just lint              # Run all linters.
just lint-client       # Lint the client code with Prettier and Stylelint.
just lint-server       # Lint the server code with Ruff and prek.
just makemessages      # Extract messages for translation.
just migrate           # Make migrations and migrate the demo database.
just runserver         # Run the demo development server.
just shell             # Open a shell to the demo application.
just test              # Run tests with pytest.
just test-highest-deps # Run tests against the latest Django and Wagtail.
just test-lowest-deps  # Run tests against the lowest supported Python, Django and Wagtail.
```

Run `just lint` and `just test` before opening a pull request.

## The README demo GIF

`docs/demo.gif` is recorded from the demo site by `demo/record_demo_gif.py`. It starts a throwaway demo server with a temporary
database and media folder, types into the editor with Playwright, and converts the recording with [ffmpeg](https://ffmpeg.org/).
After a change to the editor's look, re-record it:

```sh
just demo-gif
```

The embed step fetches a real YouTube video, so it needs network access.

## Writing tests

- **Package tests** live in `tests/` and run with pytest. They use the test app in `src/wagtail_non_admin_draftail/test/` (settings,
  URLs and a `Note` model). Files named `test_e2e_*.py` drive a real browser with Playwright.
- **Demo tests** live in `demo/notes/tests.py` and run with Django's test runner: `uv run ./demo/manage.py test notes`.

## Styles

The editor's CSS is compiled from the SCSS sources in `src/wagtail_non_admin_draftail/static_src/`. The compiled
`static/wagtail_non_admin_draftail/draftail.css` is committed and shipped in the package, and CI doesn't rebuild it. After editing the
SCSS, run `just build-css` and commit both files.

## Continuous integration

The project uses GitHub Actions. On every pull request, and on pushes to `master`, `stable/**` and `renovate/**` branches, CI:

- Runs the linters (Ruff, prek, Prettier and Stylelint).
- Runs the tests with coverage, Django's system checks and a missing-migrations check, for both the test app and the demo.
- Runs the tests against the lowest supported versions (Python 3.11, Django 5.2, Wagtail 7.4).
- Runs the tests against the latest versions (Python 3.14, the latest Django and Wagtail).
- Runs the tests against the remaining Django and Wagtail pairings: Python 3.12 with Wagtail 7.4 and Django 6.0, and Python 3.13 with
  Wagtail 8 and Django 5.2. These rows are pinned in `.github/workflows/test.yml` and updated by hand when a new Wagtail or Django
  release changes the supported range.

There's also a scheduled job (Monday, Wednesday and Friday nights, UTC) that tests each new stable Wagtail release once, so
compatibility problems show up before `uv.lock` catches up. CodeQL and zizmor scan the code and the workflows, and Renovate keeps dependencies up to date.

## Code review

Create a pull request with your changes so a maintainer can review it. Give a summary of the purpose of the change and any steps the
reviewer needs to take to test it, and please include tests.

## Translating

Translations are managed with [Django's built-in internationalization framework](https://docs.djangoproject.com/en/stable/topics/i18n/translation/).
The translation files live in `src/wagtail_non_admin_draftail/locale/`.

### Authoring guidance for new strings

When adding new translatable strings, use the right translation functions in your code, such as `ngettext` for pluralization or
`pgettext` for context-specific translations. Use `{% blocktrans trimmed %}` in templates for multi-line strings. The `trimmed` option
removes leading and trailing whitespace from the translated string.

Principles for writing translatable strings:

- **Use decent English:** a string written in poor or ambiguous English is hard to understand and translate. Add a
  `# Translators: ...` comment above the string to clarify its meaning if needed.
- **Entire sentences:** make each translatable string a complete sentence. Don't build sentences by interpolating or concatenating
  verbs and nouns; that makes grammatically correct translations hard or impossible.
- **Prefer named placeholders:** use named placeholders (`%(placeholder_name)s`) instead of positional ones (`%s`). This tells
  translators what the value is and lets them reorder placeholders.

For detailed code examples, see Wagtail's guide to
[marking strings for translation](https://docs.wagtail.org/en/stable/contributing/translations.html#marking-strings-for-translation).

### Updating all translations

Contributors don't need to update the translations after changing or adding strings, since that often causes git conflicts. If you do
want to update all translations, run:

```sh
just makemessages
```

### Adding a new language

[Find your ISO 639 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) and run:

```sh
just makemessages -l=<language_code>
```

Then translate the generated `src/wagtail_non_admin_draftail/locale/<language_code>/LC_MESSAGES/django.po` file.
[Poedit](https://poedit.net/) is a popular tool for editing `.po` files.

### Compiling translations

The repo only contains the human-readable `.po` files. To use the translations locally, compile them into `.mo` files:

```sh
just compilemessages
```

The release workflow compiles them automatically, so published packages always include the `.mo` files.

## Releases

On the `master` branch:

1. Update the version number in `pyproject.toml`.
2. Move the `[Unreleased]` entries in the [CHANGELOG](CHANGELOG.md) under the new version and date.
3. Commit, tag and push the release: `git commit -m "Release vX.Y.Z" && git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push --follow-tags`.

Pushing the tag starts the `Release` workflow (`.github/workflows/publish.yml`). It first checks that the tag matches the version in
`pyproject.toml` and that the CHANGELOG has a section for that version, and stops if either is wrong. Then it runs the tests, compiles
the translations, builds and smoke-tests the wheel and sdist, and publishes them to PyPI. Once PyPI has accepted them, it creates
the GitHub release, with the CHANGELOG section as release notes and the wheel and sdist attached. You don't create the release by
hand.

### One-time maintainer setup

The release and security tooling needs a few settings that live outside the repo:

- **PyPI trusted publisher:** on PyPI, add a trusted publisher for owner `timonweb`, repository `wagtail-non-admin-draftail`, workflow
  `publish.yml` and environment `pypi`.
- **GitHub environment:** in the repo settings, create an environment called `pypi`. Add required reviewers if you want a manual
  approval step before publishing.
- **Renovate:** install the [Renovate GitHub app](https://github.com/apps/renovate) on the repository.
- **CodeQL:** keep CodeQL's "default setup" turned off in the repo's code security settings, because `codeql-analysis.yml` runs the
  advanced setup.
- **Private vulnerability reporting:** turn it on in the repo's security settings, so [SECURITY.md](SECURITY.md) works.
