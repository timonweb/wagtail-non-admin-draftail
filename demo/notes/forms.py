from django import forms

from wagtail_non_admin_draftail.widgets import NonAdminDraftailRichTextArea

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "body"]
        widgets = {"body": NonAdminDraftailRichTextArea}
