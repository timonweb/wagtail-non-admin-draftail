"""
Django settings for the wagtail_non_admin_draftail test app.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/
"""

import os

import dj_database_url


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(PROJECT_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "not-a-secure-key"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]


INSTALLED_APPS = [
    "wagtail_non_admin_draftail",
    "wagtail_non_admin_draftail.test",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "modelcluster",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "wagtail_non_admin_draftail.test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# Don't use the intentionally slow default password hasher.
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///test_wagtail_non_admin_draftail.db"
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "test-static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "test-media")
MEDIA_URL = "/media/"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "form"

WAGTAIL_SITE_NAME = "Wagtail non-admin Draftail test site"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

WAGTAILEMBEDS_FINDERS = [
    {"class": "wagtail_non_admin_draftail.test.embed_finders.YouTubeTestEmbedFinder"}
]
