import pytest

from playwright.sync_api import expect

from .conftest import FORM_PAGE_URL


# Regression test for GitHub issue #21: closing a chooser modal without choosing
# anything used to leave the editor read-only.
@pytest.mark.django_db
@pytest.mark.parametrize("button", ["LINK", "IMAGE", "DOCUMENT", "EMBED"])
def test_closing_modal_leaves_editor_editable(
    ensure_root_collection, authenticated_page, live_server, button
):
    authenticated_page.goto(live_server + FORM_PAGE_URL)
    textbox = authenticated_page.locator('[role="textbox"]')

    textbox.fill("before")
    authenticated_page.dblclick('.public-DraftEditor-content [data-text="true"]')
    authenticated_page.click(f"button[name={button}]")

    modal = authenticated_page.locator(".Non-Admin-Draftail__modal")
    expect(modal).to_be_visible()
    modal.locator('[data-action="close"]').click()
    expect(modal).to_be_hidden()

    expect(textbox).to_have_attribute("contenteditable", "true")
    textbox.click()
    authenticated_page.keyboard.press("End")
    authenticated_page.keyboard.type(" after")
    expect(textbox).to_contain_text("before after")
