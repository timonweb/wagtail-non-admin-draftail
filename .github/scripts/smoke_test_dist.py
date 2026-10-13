#!/usr/bin/env python
"""
Smoke-test a built wheel or sdist before publishing.

Run it in an isolated environment where only the built artifact is installed:

    uv run --isolated --no-project --with dist/*.whl .github/scripts/smoke_test_dist.py

The test suite can't run against the artifact because the test app is excluded
from it, so this compares the installed package with the source tree instead:
every module, template and static file in `src/` must be importable or
resolvable from the installed package.
"""

import importlib
import sys

from pathlib import Path

import django

from django.conf import settings


PACKAGE = "wagtail_non_admin_draftail"
SOURCE_DIR = Path(__file__).resolve().parents[2] / "src" / PACKAGE
# Mirrors `source-exclude` in pyproject.toml.
EXCLUDED_TOP_LEVEL_DIRS = {"test", "static_src"}


def is_shipped(file):
    parts = file.relative_to(SOURCE_DIR).parts
    return (
        file.is_file()
        and not file.name.startswith(".")
        and parts[0] not in EXCLUDED_TOP_LEVEL_DIRS
        and "__pycache__" not in parts
    )


def source_files(subdir, pattern):
    root = SOURCE_DIR / subdir
    files = sorted(
        file.relative_to(root) for file in root.rglob(pattern) if is_shipped(file)
    )
    # An empty list would make every check below pass without checking anything.
    if not files:
        sys.exit(f"Smoke test failed: no {pattern} files found under {root}")
    return files


def configure():
    settings.configure(
        DEBUG=False,
        SECRET_KEY="smoke-test",  # noqa: S106
        ROOT_URLCONF=f"{PACKAGE}.urls",
        INSTALLED_APPS=[
            PACKAGE,
            "wagtail.embeds",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.admin",
            "wagtail",
            "taggit",
            "modelcluster",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ],
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ]
                },
            }
        ],
        STATIC_URL="/static/",
        WAGTAIL_SITE_NAME="Smoke test",
        WAGTAILADMIN_BASE_URL="http://localhost",
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    )
    django.setup()


def check_installed_location():
    package = importlib.import_module(PACKAGE)
    location = Path(package.__file__).resolve()
    if location.is_relative_to(SOURCE_DIR):
        return [f"{PACKAGE} was imported from the source tree ({location})"]
    print(f"Testing {PACKAGE} installed at {location.parent}")
    return []


def check_modules():
    errors = []
    for file in source_files(".", "*.py"):
        module = ".".join((PACKAGE, *file.with_suffix("").parts))
        module = module.removesuffix(".__init__")
        try:
            importlib.import_module(module)
        except ImportError as e:
            errors.append(f"module {module}: {e}")
    return errors


def check_templates():
    from django.template import TemplateDoesNotExist
    from django.template.loader import get_template

    errors = []
    for file in source_files("templates", "*.html"):
        try:
            get_template(file.as_posix())
        except TemplateDoesNotExist:
            errors.append(f"template {file.as_posix()} is missing")
    return errors


def check_static():
    from django.contrib.staticfiles import finders

    return [
        f"static file {file.as_posix()} is missing"
        for file in source_files("static", "*")
        if finders.find(file.as_posix()) is None
    ]


def check_urls():
    from django.urls import NoReverseMatch, reverse

    urls = importlib.import_module(f"{PACKAGE}.urls")
    errors = []
    for pattern in urls.urlpatterns:
        kwargs = dict.fromkeys(pattern.pattern.converters, 1)
        try:
            reverse(pattern.name, kwargs=kwargs)
        except NoReverseMatch as e:
            errors.append(f"url {pattern.name}: {e}")
    return errors


def main():
    configure()

    from django.core.management import call_command

    call_command("check", fail_level="ERROR")

    errors = [
        *check_installed_location(),
        *check_modules(),
        *check_templates(),
        *check_static(),
        *check_urls(),
    ]
    if errors:
        print("Smoke test failed:", *errors, sep="\n  ", file=sys.stderr)
        sys.exit(1)
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
