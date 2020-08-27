import pytest
from django.urls import reverse

FORM_PAGE_URL = reverse("example:form")


@pytest.mark.django_db
def test_it(authenticated_page, live_server):
    authenticated_page.goto(live_server + FORM_PAGE_URL)
    authenticated_page.click("button[name=IMAGE]")
    authenticated_page.waitForSelector("text=Upload an image")
    file_input = authenticated_page.querySelector('.Non-Admin-Draftail__content form [type=file]')
    file_input.setInputFiles('example/tests/seed/example.png')
    authenticated_page.click('.Non-Admin-Draftail__content form [type=submit]')
    authenticated_page.waitForSelector("text=Choose a format")
    authenticated_page.click('label[for=id_image-chooser-insertion-format_0]')
    authenticated_page.click('.Non-Admin-Draftail__content form [type=submit]')
    authenticated_page.waitForSelector('.Draftail-Editor img.MediaBlock__img')
