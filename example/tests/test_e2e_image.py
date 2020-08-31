import pytest
from wagtail.core.models import Collection
from wagtail.images import get_image_model

from .conftest import FORM_PAGE_URL


@pytest.mark.django_db
def test_image_button(ensure_root_collection, authenticated_page, live_server):
    authenticated_page.goto(live_server + FORM_PAGE_URL)

    # Click image button in the editor
    authenticated_page.click("button[name=IMAGE]")

    # Wait for modal to appear
    authenticated_page.waitForSelector(".modal", state="visible")
    authenticated_page.waitForSelector("text=Upload an image", state="visible")

    # Upload example file
    file_input = authenticated_page.querySelector(".modal form [type=file]")
    file_input.setInputFiles("example/tests/seed/example.png")

    # Submit the form
    authenticated_page.click(".modal form [type=submit]")

    # User sees the next modal "Choose a format"
    authenticated_page.waitForSelector("text=Choose a format")

    # Select full width
    authenticated_page.click("label[for=id_image-chooser-insertion-format_0]")

    # Submit choose format
    authenticated_page.click(".Non-Admin-Draftail__content form [type=submit]")

    # Modal is hidden
    authenticated_page.waitForSelector(".modal", state="hidden")

    # Make sure image is embedded in draftail
    authenticated_page.waitForSelector(".Draftail-Editor img.MediaBlock__img")

    # Click on image again and make sure modal is show again
    # We test if the toolbar was properly unlocked.
    authenticated_page.click("button[name=IMAGE]")
    authenticated_page.waitForSelector(".modal", state="visible")
    authenticated_page.waitForSelector("text=Upload an image", state="visible")

    # Ensure uploaded image is added to "Public uploads" collection
    image = get_image_model().objects.last()
    assert image.collection == Collection.objects.get(name="Public uploads")
