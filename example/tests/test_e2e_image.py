import os

import pytest
from wagtail.images import get_image_model
from wagtail.models import Collection

from .conftest import FORM_PAGE_URL


@pytest.mark.django_db
def test_image_button(ensure_root_collection, authenticated_page, live_server):
    authenticated_page.goto(live_server + FORM_PAGE_URL)

    authenticated_page.fill('[role="textbox"]', "test whatever")
    authenticated_page.dblclick('.public-DraftEditor-content [data-text="true"]')
    authenticated_page.click("button[name=IMAGE]")

    # Wait for modal to appear
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    authenticated_page.wait_for_selector("text=Upload an image", state="visible")

    # Upload example file
    file_input = authenticated_page.query_selector(".Non-Admin-Draftail__modal form [type=file]")
    file_input.set_input_files(os.path.join(os.path.dirname(__file__), "seed/example.png"))

    # Submit the form
    authenticated_page.click(".Non-Admin-Draftail__modal form [type=submit]")

    # User sees the next modal "Choose a format"
    authenticated_page.wait_for_selector("text=Choose a format")

    # Select full width
    authenticated_page.click("label[for=id_image-chooser-insertion-format_0]")

    # Submit choose format
    authenticated_page.click(".Non-Admin-Draftail__content form [type=submit]")

    # Modal is hidden
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="hidden")

    # Make sure image is embedded in draftail
    assert authenticated_page.query_selector(".Draftail-Editor .MediaBlock__img")

    # Ensure uploaded image is added to "Public uploads" collection
    image = get_image_model().objects.last()
    assert image.collection == Collection.objects.get(name="Public uploads")
