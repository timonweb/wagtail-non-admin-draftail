from django import forms
from wagtail.admin.rich_text import DraftailRichTextArea

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text"]

        widgets = {
            "text": DraftailRichTextArea
        }
