from pathlib import Path

import pytest

from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import NoReverseMatch, reverse
from wagtail.documents import get_document_model
from wagtail.embeds.finders.embedly import (
    AccessDeniedEmbedlyException,
    EmbedlyException,
)
from wagtail.images import get_image_model
from wagtail.models import Collection


SEED_DIR = Path(__file__).parent / "seed"
YOUTUBE_URL = "https://www.youtube.com/watch?v=IMNFjrQ5OY4"


def url(name, *args):
    return reverse(f"wagtail_non_admin_draftail:{name}", args=args)


def seed_upload(filename, content_type):
    return SimpleUploadedFile(
        filename, (SEED_DIR / filename).read_bytes(), content_type=content_type
    )


@pytest.fixture
def public_collection(ensure_root_collection):
    return Collection.get_first_root_node().add_child(name="Public uploads")


@pytest.fixture
def private_collection(ensure_root_collection):
    return Collection.get_first_root_node().add_child(name="Private")


def make_image(collection):
    with (SEED_DIR / "example.png").open("rb") as f:
        return get_image_model().objects.create(
            title="Example",
            file=ImageFile(f, name="example.png"),
            collection=collection,
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("name", "args"),
    [
        ("external-link", ()),
        ("email-link", ()),
        ("phone-link", ()),
        ("anchor-link", ()),
        ("image-chooser-and-upload", ()),
        ("image-select-format", (1,)),
        ("embed-chooser", ()),
        ("embed-upload", ()),
        ("document-chooser", ()),
        ("document-upload", ()),
    ],
)
def test_anonymous_users_are_redirected_to_login(client, name, args):
    response = client.get(url(name, *args))

    assert response.status_code == 302
    assert response["Location"].startswith(reverse("login"))


def test_document_chosen_endpoint_is_removed():
    with pytest.raises(NoReverseMatch):
        url("document-chosen", 1)


@pytest.mark.django_db
def test_image_upload_saves_to_public_collection_and_asks_for_format(
    logged_in_client, ensure_root_collection
):
    response = logged_in_client.post(
        url("image-chooser-and-upload"),
        {
            "image-chooser-upload-title": "Example",
            "image-chooser-upload-file": seed_upload("example.png", "image/png"),
        },
    )

    assert response.json()["step"] == "select_format"
    image = get_image_model().objects.get()
    assert image.collection.name == "Public uploads"
    assert image.file_size > 0
    assert image.file_hash


@pytest.mark.django_db
@pytest.mark.parametrize(
    "file_field",
    [
        {},
        {"image-chooser-upload-file": seed_upload("example.txt", "text/plain")},
    ],
    ids=["missing-file", "not-an-image"],
)
def test_image_upload_rejects_invalid_files(
    logged_in_client, ensure_root_collection, file_field
):
    response = logged_in_client.post(
        url("image-chooser-and-upload"),
        {"image-chooser-upload-title": "Example", **file_field},
    )

    data = response.json()
    assert data["step"] == "choose"
    assert "errorlist" in data["html"]
    assert not get_image_model().objects.exists()


@pytest.mark.django_db
def test_image_select_format_returns_editor_data_for_public_image(
    logged_in_client, public_collection
):
    image = make_image(public_collection)

    assert logged_in_client.get(url("image-select-format", image.id)).status_code == 200

    response = logged_in_client.post(
        url("image-select-format", image.id),
        {
            "image-chooser-insertion-format": "fullwidth",
            "image-chooser-insertion-alt_text": "An example",
        },
    )

    data = response.json()
    assert data["step"] == "chosen"
    assert data["result"]["id"] == image.id
    assert data["result"]["alt"] == "An example"
    assert data["result"]["format"] == "fullwidth"
    assert data["result"]["preview"]["url"]


@pytest.mark.django_db
def test_image_select_format_hides_images_outside_public_collection(
    logged_in_client, private_collection
):
    image = make_image(private_collection)

    assert logged_in_client.get(url("image-select-format", image.id)).status_code == 404


@pytest.mark.django_db
def test_image_select_format_unknown_image_is_not_found(logged_in_client):
    assert logged_in_client.get(url("image-select-format", 999)).status_code == 404


@pytest.mark.django_db
def test_document_upload_saves_to_public_collection(
    logged_in_client, ensure_root_collection
):
    response = logged_in_client.post(
        url("document-upload"),
        {
            "document-chooser-upload-title": "Example",
            "document-chooser-upload-file": seed_upload("example.txt", "text/plain"),
        },
    )

    data = response.json()
    assert data["step"] == "chosen"
    document = get_document_model().objects.get()
    assert document.collection.name == "Public uploads"
    assert data["result"]["title"] == "Example"
    assert data["result"]["url"] == document.url
    assert data["result"]["filename"] == document.filename


@pytest.mark.django_db
def test_document_upload_requires_a_file(logged_in_client, ensure_root_collection):
    response = logged_in_client.post(
        url("document-upload"), {"document-chooser-upload-title": "Example"}
    )

    data = response.json()
    assert data["step"] == "choose"
    assert "errorlist" in data["html"]
    assert not get_document_model().objects.exists()


@pytest.mark.django_db
def test_embed_upload_returns_embed_data(logged_in_client):
    response = logged_in_client.post(
        url("embed-upload"), {"embed-chooser-url": YOUTUBE_URL}
    )

    data = response.json()
    assert data["step"] == "embed_chosen"
    assert data["embed_data"]["url"] == YOUTUBE_URL
    assert data["embed_data"]["providerName"] == "YouTube"
    assert "IMNFjrQ5OY4" in data["embed_data"]["thumbnail"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("embed_url", "error"),
    [
        ("https://example.com/not-embeddable", "Cannot find an embed for this URL."),
        ("not-a-url", "Please enter a valid URL"),
    ],
)
def test_embed_upload_shows_url_errors(logged_in_client, embed_url, error):
    response = logged_in_client.post(
        url("embed-upload"), {"embed-chooser-url": embed_url}
    )

    data = response.json()
    assert data["step"] == "chooser"
    assert error in data["html"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (AccessDeniedEmbedlyException, "problem with your embedly API key"),
        (EmbedlyException, "error with Embedly while trying to embed this URL"),
    ],
)
def test_embed_upload_shows_provider_errors(
    logged_in_client, monkeypatch, exception, error
):
    def raise_provider_error(url):
        raise exception

    monkeypatch.setattr(
        "wagtail_non_admin_draftail.views.embed.embed_to_editor_html",
        raise_provider_error,
    )

    response = logged_in_client.post(
        url("embed-upload"), {"embed-chooser-url": YOUTUBE_URL}
    )

    data = response.json()
    assert data["step"] == "chooser"
    assert error in data["html"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("name", "prefix", "fields", "expected_url"),
    [
        (
            "external-link",
            "external-link-chooser",
            {"url": "https://example.com/"},
            "https://example.com/",
        ),
        (
            "email-link",
            "email-link-chooser",
            {"email_address": "someone@example.com"},
            "mailto:someone@example.com",
        ),
        (
            "phone-link",
            "phone-link-chooser",
            {"phone_number": "+15550100"},
            "tel:+15550100",
        ),
        ("anchor-link", "anchor-link-chooser", {"url": "section-2"}, "#section-2"),
    ],
)
def test_link_choosers_return_link(
    logged_in_client, name, prefix, fields, expected_url
):
    response = logged_in_client.post(
        url(name), {f"{prefix}-{key}": value for key, value in fields.items()}
    )

    data = response.json()
    assert data["step"] == "external_link_chosen"
    assert data["result"]["url"] == expected_url


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("name", "prefix", "fields", "step"),
    [
        (
            "external-link",
            "external-link-chooser",
            {"url": "not a url"},
            "external_link",
        ),
        (
            "email-link",
            "email-link-chooser",
            {"email_address": "not-an-email"},
            "email_link",
        ),
    ],
)
def test_link_choosers_reject_invalid_input(
    logged_in_client, name, prefix, fields, step
):
    response = logged_in_client.post(
        url(name), {f"{prefix}-{key}": value for key, value in fields.items()}
    )

    data = response.json()
    assert data["step"] == step
    assert "errorlist" in data["html"]
