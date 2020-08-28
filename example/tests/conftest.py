import time

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse

DEFAULT_TEST_PASSWORD = "testuser"
FORM_PAGE_URL = reverse("example:form")


@pytest.fixture
def user(django_user_model, faker):
    return django_user_model.objects.create(username=faker.email(), password=make_password(DEFAULT_TEST_PASSWORD))


@pytest.fixture()
def authenticated_page(user, page, live_server):
    return _log_in_user(page, user, DEFAULT_TEST_PASSWORD, live_server.url)


def _log_in_user(page, user, password, base_url):
    page.goto(base_url + reverse("login"))
    page.fill("[name=username]", user.username)
    page.fill("[name=password]", password)
    page.click("form [type=submit]")
    return page
