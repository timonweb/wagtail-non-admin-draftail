from django import forms
from wagtail.admin.rich_text import DraftailRichTextArea


class ExampleForm(forms.Form):
    body = forms.CharField(widget=DraftailRichTextArea)
