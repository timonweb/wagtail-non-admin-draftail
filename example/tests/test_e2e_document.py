import os

import pytest
from wagtail.core.models import Collection
from wagtail.documents import get_document_model

from .conftest import FORM_PAGE_URL


@pytest.mark.django_db
def test_document_button(ensure_root_collection, authenticated_page, live_server):
    authenticated_page.goto(live_server + FORM_PAGE_URL)

    # Click image button in the editor
    authenticated_page.fill('[role="textbox"]', "test whatever")
    authenticated_page.dblclick('.public-DraftEditor-content [data-text="true"]')
    authenticated_page.click("button[name=DOCUMENT]")

    # Wait for modal to appear
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    authenticated_page.wait_for_selector("text=Upload a document", state="visible")

    # Upload example file
    file_input = authenticated_page.query_selector(
        ".Non-Admin-Draftail__modal form [type=file]"
    )
    file_input.set_input_files(
        os.path.join(os.path.dirname(__file__), "seed/example.txt")
    )

    # Name example file
    authenticated_page.fill(".Non-Admin-Draftail__modal form [type=text]", "whatever")

    # Submit the form
    authenticated_page.click(".Non-Admin-Draftail__modal form [type=submit]")

    # Modal is hidden
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="hidden")

    # Make sure document is embedded in draftail
    file_embed = authenticated_page.query_selector(".Draftail-Editor a.TooltipEntity")
    assert "whatever" == file_embed.text_content(), "Uploaded file has name set"
    assert "example" in file_embed.get_attribute("href"), "Embed links to uploaded file"

    # Ensure uploaded document is added to "Public uploads" collection
    document = get_document_model().objects.last()
    assert document.collection == Collection.objects.get(name="Public uploads")
