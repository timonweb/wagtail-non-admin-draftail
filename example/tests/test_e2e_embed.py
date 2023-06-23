import pytest

from .conftest import FORM_PAGE_URL


@pytest.mark.django_db
def test_embed_button(authenticated_page, live_server):
    YOUTUBE_VIDEO_ID = "IMNFjrQ5OY4"
    authenticated_page.goto(live_server + FORM_PAGE_URL)

    # Click embed button in the editor
    authenticated_page.fill('[role="textbox"]', "test whatever")
    authenticated_page.dblclick('.public-DraftEditor-content [data-text="true"]')
    authenticated_page.click("button[name=EMBED]")

    # Wait for modal to appear
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    authenticated_page.wait_for_selector("text=Insert embed", state="visible")

    # Upload example file
    authenticated_page.fill(
        "[name=embed-chooser-url]",
        "https://www.youtube.com/watch?v=" + YOUTUBE_VIDEO_ID,
    )

    # Submit the form
    authenticated_page.click(".Non-Admin-Draftail__modal form [type=submit]")

    # Modal is hidden
    authenticated_page.wait_for_selector(".Non-Admin-Draftail__modal", state="hidden")

    # Make sure image is embedded in draftail
    image = authenticated_page.query_selector(".Draftail-Editor img.MediaBlock__img")
    assert image
    assert YOUTUBE_VIDEO_ID in image.get_attribute("src")
