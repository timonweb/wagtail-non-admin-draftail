from django import forms
from django.forms import modelform_factory
from wagtail.admin.forms.collections import BaseCollectionMemberForm
from wagtail.images.forms import formfield_for_dbfield

try:
    from wagtail.models import Collection
except ImportError:
    from wagtail.core.models import Collection

from .conf import NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME


class PublicCollectionMemberForm(BaseCollectionMemberForm):
    """
    Base form that forces user uploads into a collection named "Public uploads"
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        # self.fields['collection'].required = False

        # Get or initiate the Public uploads collection.
        try:
            public_collection = Collection.objects.get(
                name=NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME
            )
        except Collection.DoesNotExist:
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(name=NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME)
            public_collection = Collection.objects.get(
                name=NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME
            )

        self.collections = (public_collection,)

    def save(self, commit=True):
        # Set NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME collection on the uploaded file instance
        if self.instance.collection is None:
            self.instance.collection = self.collections[0]
        return super().save(commit=commit)


class PublicCollectionBaseImageForm(PublicCollectionMemberForm):
    pass


def get_image_form(model):
    fields = ("title", "file")

    return modelform_factory(
        model,
        form=PublicCollectionBaseImageForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield,
        widgets={
            "file": forms.FileInput(),
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
            "file": forms.FileInput(),
        },
    )
