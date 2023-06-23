from wagtail.admin.rich_text import DraftailRichTextArea


class NonAdminDraftailRichTextArea(DraftailRichTextArea):
    """
    This widget is a complete copy of the original DraftailRichTextArea widget,
    in most cases you don't need to use it.
    However, if you need to override the widget template and don't want to mess
    draftail widget for Wagtail admin, you might find it useful.

    Copy the template below and override it in your project, then use this widget on your
    non-admin form.
    Example:
        ```
        class NoteForm(forms.ModelForm):
            class Meta:
                model = Note
                fields = ["text"]
                widgets = {"text": NonAdminDraftailRichTextArea}
        ```
    """

    template_name = "wagtail_non_admin_draftail/widgets/non_admin_draftail_rich_text_area.html"
