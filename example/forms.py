from django import forms

from non_admin_draftail.widgets import NonAdminDraftailRichTextArea

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text"]

        widgets = {"text": NonAdminDraftailRichTextArea}
