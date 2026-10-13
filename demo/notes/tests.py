import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.documents import get_document_model

from .models import Note


def contentstate(text, bold=None):
    """Build the Draftail JSON the editor submits, optionally bolding a substring."""
    style_ranges = []
    if bold:
        style_ranges.append(
            {"offset": text.index(bold), "length": len(bold), "style": "BOLD"}
        )
    return json.dumps(
        {
            "blocks": [
                {
                    "key": "a1b2c",
                    "type": "unstyled",
                    "depth": 0,
                    "text": text,
                    "inlineStyleRanges": style_ranges,
                    "entityRanges": [],
                }
            ],
            "entityMap": {},
        }
    )


class NoteReadTests(TestCase):
    def test_home_links_to_notes(self):
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            f'<a href="{reverse("notes:list")}">Browse the notes</a>',
            html=True,
        )

    def test_list_shows_titles(self):
        Note.objects.create(title="First note", body="<p>One</p>")
        Note.objects.create(title="Second note", body="<p>Two</p>")

        response = self.client.get(reverse("notes:list"))

        self.assertContains(response, "First note")
        self.assertContains(response, "Second note")

    def test_list_empty_state(self):
        response = self.client.get(reverse("notes:list"))

        self.assertContains(response, "No notes yet.")

    def test_detail_renders_rich_text(self):
        # Only a name: the link renders from the document's id and filename.
        document = get_document_model().objects.create(
            title="Spec", file="documents/spec.txt"
        )
        note = Note.objects.create(
            title="Rich",
            body=(
                "<p>Hello <b>world</b>, read the "
                f'<a linktype="document" id="{document.pk}">spec</a></p>'
            ),
        )

        response = self.client.get(note.get_absolute_url())

        self.assertContains(response, "<b>world</b>", html=True)
        # Stored rich text only becomes a real link through the richtext filter.
        self.assertContains(response, f'<a href="{document.url}">spec</a>', html=True)

    def test_detail_unknown_note_is_404(self):
        response = self.client.get(reverse("notes:detail", args=[999]))

        self.assertEqual(response.status_code, 404)


class NoteLoginRequiredTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Original", body="<p>Original</p>")

    def assert_redirects_to_login(self, response, url):
        self.assertRedirects(
            response,
            f"{reverse('wagtailadmin_login')}?next={url}",
            fetch_redirect_response=False,
        )

    def test_anonymous_cannot_open_create(self):
        url = reverse("notes:create")

        self.assert_redirects_to_login(self.client.get(url), url)

    def test_anonymous_cannot_create(self):
        url = reverse("notes:create")

        response = self.client.post(
            url, {"title": "Sneaky", "body": contentstate("Sneaky")}
        )

        self.assert_redirects_to_login(response, url)
        self.assertFalse(Note.objects.filter(title="Sneaky").exists())

    def test_anonymous_cannot_open_edit(self):
        url = reverse("notes:update", args=[self.note.pk])

        self.assert_redirects_to_login(self.client.get(url), url)

    def test_anonymous_cannot_edit(self):
        url = reverse("notes:update", args=[self.note.pk])

        response = self.client.post(
            url, {"title": "Changed", "body": contentstate("Changed")}
        )

        self.assert_redirects_to_login(response, url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Original")
        self.assertEqual(self.note.body, "<p>Original</p>")


class NoteWriteTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_user("editor"))

    def test_create_page_loads_the_editor(self):
        response = self.client.get(reverse("notes:create"))

        # draftail_media.html loads the admin scripts and the package's modal code…
        self.assertContains(response, "wagtail_non_admin_draftail/modal-workflow.js")
        self.assertContains(response, "wagtail_non_admin_draftail/draftail.css")
        # …{{ form.media }} loads the editor itself…
        self.assertContains(response, "wagtailadmin/js/draftail.js")
        # …and the widget points its choosers at the package's views.
        self.assertContains(
            response, reverse("wagtail_non_admin_draftail:external-link")
        )
        self.assertContains(
            response, reverse("wagtail_non_admin_draftail:image-chooser-and-upload")
        )

    def test_create_saves_rich_text_and_redirects(self):
        response = self.client.post(
            reverse("notes:create"),
            {"title": "Fresh", "body": contentstate("Hello world", bold="world")},
        )

        note = Note.objects.get(title="Fresh")
        self.assertRedirects(response, note.get_absolute_url())
        self.assertInHTML("<b>world</b>", note.body)

    def test_create_without_title_shows_error(self):
        response = self.client.post(
            reverse("notes:create"), {"title": "", "body": contentstate("Body")}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "title", "This field is required."
        )
        self.assertFalse(Note.objects.exists())

    def test_edit_updates_note(self):
        note = Note.objects.create(title="Before", body="<p>Before</p>")

        response = self.client.post(
            reverse("notes:update", args=[note.pk]),
            {"title": "After", "body": contentstate("After")},
        )

        self.assertRedirects(response, note.get_absolute_url())
        note.refresh_from_db()
        self.assertEqual(note.title, "After")
        self.assertInHTML('<p data-block-key="a1b2c">After</p>', note.body)

    def test_edit_unknown_note_is_404(self):
        response = self.client.get(reverse("notes:update", args=[999]))

        self.assertEqual(response.status_code, 404)
