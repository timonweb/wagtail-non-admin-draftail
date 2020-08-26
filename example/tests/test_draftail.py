import pytest
from django.urls import reverse

FORM_PAGE_URL = reverse("example:form")


@pytest.mark.django_db
def test_it(authenticated_page, live_server):
    authenticated_page.goto(live_server.url + FORM_PAGE_URL)
    authenticated_page.click("button[name=IMAGE]")
    breakpoint()
