from django.urls import reverse
from wagtail.admin.rich_text import DraftailRichTextArea


class NonAdminDraftailRichTextArea(DraftailRichTextArea):
    """
    This widget is a modified version of the original DraftailRichTextArea widget.
    You must use it on forms to enable Draftail functionality on non-admin pages.

    To use it, override widgets in your form.
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

    def get_context(self, name, value, attrs):
        self.replace_admin_chooser_urls(self.options)
        return super().get_context(name, value, attrs)

    def replace_admin_chooser_urls(self, options):
        chooser_urls_map = {
            "imageChooser": "wagtail_non_admin_draftail:image-chooser-and-upload",
            "pageChooser": "wagtail_non_admin_draftail:external-link",
            "externalLinkChooser": "wagtail_non_admin_draftail:external-link",
            "emailLinkChooser": "wagtail_non_admin_draftail:email-link",
            "phoneLinkChooser": "wagtail_non_admin_draftail:phone-link",
            "anchorLinkChooser": "wagtail_non_admin_draftail:anchor-link",
            "embedsChooser": "wagtail_non_admin_draftail:embed-chooser",
            "documentChooser": "wagtail_non_admin_draftail:document-chooser",
        }

        def recursive_replace_urls(obj):
            for key in obj.get("chooserUrls", {}).keys():
                if new_urlname := chooser_urls_map.get(key):
                    obj["chooserUrls"][key] = reverse(new_urlname)

            for entity_type in obj.get("entityTypes", []):
                recursive_replace_urls(entity_type)

            return obj

        recursive_replace_urls(options)
