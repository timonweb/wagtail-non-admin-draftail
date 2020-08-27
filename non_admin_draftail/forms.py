from django import forms
from django.forms import modelform_factory
from wagtail.admin.forms.collections import BaseCollectionMemberForm
from wagtail.core.models import Collection
from wagtail.images.forms import formfield_for_dbfield


class PublicCollectionMemberForm(BaseCollectionMemberForm):
    """
    Base form that forces user uploads into a collection named "Public uploads"
    """
    def __init__(self, *args, **kwargs):
        kwargs.pop('user')
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        # Get or initiate the Public uploads collection.
        try:
            public_collection = Collection.objects.get(name="Public uploads")
        except Collection.DoesNotExist:
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(name="Public uploads")
            public_collection = Collection.objects.get(name="Public uploads")

        self.collections = [public_collection]

    def save(self, commit=True):
        # Set "Public uploads" collection on the uploaded file instance
        if self.instance.collection is None:
            self.instance.collection = self.collections[0]
        return super().save(commit=commit)


class PublicCollectionBaseImageForm(PublicCollectionMemberForm):
    pass


def get_image_form(model):
    fields = (
        "title",
        "file",
        "collection"
    )

    return modelform_factory(
        model,
        form=PublicCollectionBaseImageForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield,
        widgets={
            "file": forms.FileInput(),
            # Collection input should not be visible to end user.
            "collection": forms.HiddenInput(),
        },
    )


class PublicCollectionBaseDocumentForm(PublicCollectionMemberForm):
    pass


def get_document_form(model):
    fields = ("title", "file", "collection", )

    return modelform_factory(
        model,
        form=PublicCollectionBaseDocumentForm,
        fields=fields,
        widgets={
            'file': forms.FileInput(),
            # Collection input should not be visible to end user.
            'collection': forms.HiddenInput(),
        })
