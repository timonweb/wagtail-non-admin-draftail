from django import forms
from django.forms import modelform_factory
from wagtail.admin.forms.collections import BaseCollectionMemberForm
from wagtail.images.forms import formfield_for_dbfield
from wagtail.models import Collection

from .conf import WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME


class PublicCollectionMemberForm(BaseCollectionMemberForm):
    """
    Base form that forces user uploads into a collection named "Public uploads"
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        # Point the w-sync controller on the file input at this form's (prefixed)
        # title field, as Wagtail's BaseImageForm/BaseDocumentForm do.
        self.fields["file"].widget.attrs["data-w-sync-target-value"] = (
            f"#{self['title'].id_for_label}"
        )

        # Get or initiate the Public uploads collection.
        try:
            public_collection = Collection.objects.get(
                name=WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME
            )
        except Collection.DoesNotExist:
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(name=WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME)
            public_collection = Collection.objects.get(
                name=WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME
            )

        self.collections = (public_collection,)

    def save(self, commit=True):
        # Set WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME collection on the uploaded file instance
        if self.instance.collection is None:
            self.instance.collection = self.collections[0]
        return super().save(commit=commit)


class PublicCollectionBaseImageForm(PublicCollectionMemberForm):
    pass


def _sync_title_file_input(sync_event_name):
    """
    A file input that prefills the title field from the chosen file's name, using
    the same Stimulus w-sync wiring as Wagtail's own image and document forms.
    """
    return forms.FileInput(
        attrs={
            "data-controller": "w-sync",
            "data-action": "input->w-sync#apply",
            "data-w-sync-bubbles-param": "true",
            "data-w-sync-name-value": sync_event_name,
            "data-w-sync-normalize-value": "true",
        }
    )


def get_image_form(model):
    fields = ("title", "file")

    return modelform_factory(
        model,
        form=PublicCollectionBaseImageForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield,
        widgets={
            "file": _sync_title_file_input("wagtail:images-upload"),
        },
    )


class PublicCollectionBaseDocumentForm(PublicCollectionMemberForm):
    pass


def get_document_form(model):
    fields = ("title", "file")

    return modelform_factory(
        model,
        form=PublicCollectionBaseDocumentForm,
        fields=fields,
        widgets={
            "file": _sync_title_file_input("wagtail:documents-upload"),
        },
    )
