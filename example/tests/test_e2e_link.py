import pytest

from .conftest import FORM_PAGE_URL


@pytest.mark.django_db
def test_link_button(authenticated_page, live_server):
    URL = "https://timonweb.com/"
    TEXT = "timonweb.com"

    authenticated_page.goto(live_server + FORM_PAGE_URL)

    # Click image button in the editor
    authenticated_page.click("button[name=LINK]")

    # Wait for modal to appear
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    authenticated_page.wait_for_selector("text=Add a link", state="visible")

    # Upload example file
    authenticated_page.fill("[name=external-link-chooser-url]", URL)
    authenticated_page.fill("[name=external-link-chooser-link_text]", TEXT)

    # Submit the form
    authenticated_page.click(".Non-Admin-Draftail__modal form [type=submit]")

    # Modal is hidden
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="hidden")

    # Make sure link is embedded in draftail
    inserted_link = authenticated_page.query_selector(
        ".Draftail-Editor a.TooltipEntity"
    )
    assert TEXT == inserted_link.text_content(), "Link has text set"
    assert URL == inserted_link.get_attribute("href"), "Url is what user set"

    # Click on image again and make sure modal is show again
    # We test if the toolbar was properly unlocked.
    authenticated_page.click("button[name=LINK]")
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    authenticated_page.wait_for_selector("text=Add a link", state="visible")
