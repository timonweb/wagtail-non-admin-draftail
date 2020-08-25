from django import forms
from django.forms import modelform_factory
from wagtail.admin import widgets
from wagtail.core.models import Collection
from wagtail.documents.forms import BaseDocumentForm
from wagtail.images.forms import BaseImageForm, formfield_for_dbfield


class PublicCollectionBaseImageForm(BaseImageForm):
    def save(self, commit=True):
        try:
            public_collection = Collection.objects.get(name="Public uploads")
        except Collection.DoesNotExist:
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(name="Public uploads")
            public_collection = Collection.objects.get(name="Public uploads")
        self.instance.collection = public_collection
        return super().save(commit=commit)


def get_image_form(model):
    fields = (
        "title",
        "file",
    )
    if "collection" not in fields:
        fields = list(fields) + ["collection"]

    return modelform_factory(
        model,
        form=PublicCollectionBaseImageForm,
        fields=fields,
        formfield_callback=formfield_for_dbfield,
        widgets={"file": forms.FileInput(), "collection": forms.HiddenInput(), },
    )


class PublicCollectionBaseDocumentForm(BaseDocumentForm):
    def save(self, commit=True):
        try:
            public_collection = Collection.objects.get(name="Public uploads")
        except Collection.DoesNotExist:
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(name="Public uploads")
            public_collection = Collection.objects.get(name="Public uploads")
        self.instance.collection = public_collection
        return super().save(commit=commit)


def get_document_form(model):
    fields = ("title", "file",)
    if 'collection' not in fields:
        # force addition of the 'collection' field, because leaving it out can
        # cause dubious results when multiple collections exist (e.g adding the
        # document to the root collection where the user may not have permission) -
        # and when only one collection exists, it will get hidden anyway.
        fields = list(fields) + ['collection']

    return modelform_factory(
        model,
        form=PublicCollectionBaseDocumentForm,
        fields=fields,
        widgets={
            'file': forms.FileInput(),
            'collection': forms.HiddenInput(),
        })
