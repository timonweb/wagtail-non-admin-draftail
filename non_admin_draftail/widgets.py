from wagtail.admin.rich_text import DraftailRichTextArea


class NonAdminDraftailRichTextArea(DraftailRichTextArea):
    template_name = "non_admin_draftail/widgets/non_admin_draftail_rich_text_area.html"
