from html.parser import HTMLParser

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string


class _AssetCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("src"):
            self.urls.append(attrs["src"])
        elif tag == "link" and attrs.get("href"):
            self.urls.append(attrs["href"])


def _rendered_static_paths():
    collector = _AssetCollector()
    collector.feed(render_to_string("wagtail_non_admin_draftail/draftail_media.html"))
    return [
        url.removeprefix(settings.STATIC_URL).split("?")[0]
        for url in collector.urls
        if url.startswith(settings.STATIC_URL)
    ]


def test_draftail_media_references_only_existing_static_files():
    # A reference to a static file Wagtail has removed raises a 500 under
    # ManifestStaticFilesStorage, so every asset must resolve.
    paths = _rendered_static_paths()

    assert paths
    missing = [path for path in paths if finders.find(path) is None]
    assert missing == []


def test_draftail_media_does_not_load_removed_telepath_script():
    assert "wagtailadmin/js/telepath/telepath.js" not in _rendered_static_paths()
