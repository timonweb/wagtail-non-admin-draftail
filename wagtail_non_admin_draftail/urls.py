from django.apps import apps
from django.urls import path

from .views.link import anchor_link, email_link, external_link, phone_link

app_name = "wagtail_non_admin_draftail"

urlpatterns = [
    path("external-link/", external_link, name="external-link"),
    path("email-link/", email_link, name="email-link"),
    path("phone-link/", phone_link, name="phone-link"),
    path("anchor-link/", anchor_link, name="anchor-link"),
]

if apps.is_installed("wagtail.images"):
    from .views.image import image_chooser_and_upload, image_select_format

    urlpatterns += [
        path(
            "image-upload/", image_chooser_and_upload, name="image-chooser-and-upload"
        ),
        path(
            "image-upload/<int:image_id>/select_format/",
            image_select_format,
            name="image-select-format",
        ),
    ]

if apps.is_installed("wagtail.embeds"):
    from .views.embed import embed_chooser, embed_chooser_upload

    urlpatterns += [
        path("embed-chooser/", embed_chooser, name="embed-chooser"),
        path("embed-upload/", embed_chooser_upload, name="embed-upload"),
    ]

if apps.is_installed("wagtail.documents"):
    from .views.document import (
        document_chooser,
        document_chooser_upload,
        document_chosen,
    )

    urlpatterns += [
        path("document-chooser/", document_chooser, name="document-chooser"),
        path(
            "document-chooser/<int:document_id>/",
            document_chosen,
            name="document-chosen",
        ),
        path("document-upload/", document_chooser_upload, name="document-upload"),
    ]
