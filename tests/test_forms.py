import pytest

from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from wagtail_non_admin_draftail.forms import get_document_form, get_image_form


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("get_form", "get_model", "prefix", "sync_event"),
    [
        (get_image_form, get_image_model, "image-chooser-upload", "images-upload"),
        (
            get_document_form,
            get_document_model,
            "document-chooser-upload",
            "documents-upload",
        ),
    ],
)
def test_file_input_prefills_title_via_w_sync(
    ensure_root_collection, django_user_model, get_form, get_model, prefix, sync_event
):
    form_class = get_form(get_model())
    form = form_class(user=django_user_model(), prefix=prefix)

    attrs = form.fields["file"].widget.attrs
    assert attrs["data-controller"] == "w-sync"
    assert attrs["data-action"] == "input->w-sync#apply"
    assert attrs["data-w-sync-name-value"] == f"wagtail:{sync_event}"
    assert attrs["data-w-sync-target-value"] == f"#id_{prefix}-title"
    assert f'id="id_{prefix}-title"' in str(form["title"])
