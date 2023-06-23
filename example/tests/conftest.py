import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from wagtail.models import Collection

DEFAULT_TEST_PASSWORD = "testuser"
FORM_PAGE_URL = reverse("example:form")


@pytest.fixture()
def page(page, live_server):
    page.set_default_timeout(5000)
    page.base_url = live_server.url
    return page


@pytest.fixture
def user(django_user_model, faker):
    return django_user_model.objects.create(
        username=faker.email(), password=make_password(DEFAULT_TEST_PASSWORD)
    )


@pytest.fixture
def authenticated_page(user, page, live_server):
    return _log_in_user(page, user, DEFAULT_TEST_PASSWORD, live_server.url)


@pytest.fixture
def ensure_root_collection():
    root_collection = Collection.get_first_root_node()
    if root_collection is None:
        Collection.objects.create(
            name="Root",
            path="0001",
            depth=1,
            numchild=0,
        )


def _log_in_user(page, user, password, base_url):
    page.goto(base_url + reverse("login"))
    page.fill("[name=username]", user.username)
    page.fill("[name=password]", password)
    page.click("form [type=submit]")
    return page
