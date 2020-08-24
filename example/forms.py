from django import forms
from non_admin_draftail.widgets import NonAdminDraftailRichTextArea


class ExampleForm(forms.Form):
    body = forms.CharField(widget=NonAdminDraftailRichTextArea)

    class Meta:
        widgets = {
            "body": NonAdminDraftailRichTextArea()
        }
