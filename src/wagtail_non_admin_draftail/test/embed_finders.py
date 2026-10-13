from urllib.parse import parse_qs, urlparse

from wagtail.embeds.finders.base import EmbedFinder


class YouTubeTestEmbedFinder(EmbedFinder):
    """
    Answers YouTube watch URLs with canned oEmbed data so tests don't depend on
    the network. Any other URL is rejected, which exercises the "no embed found"
    path just like an unsupported provider would.
    """

    def accept(self, url):
        return self._video_id(url) is not None

    def find_embed(self, url, max_width=None, max_height=None):
        video_id = self._video_id(url)
        return {
            "title": "Test video",
            "author_name": "Test author",
            "provider_name": "YouTube",
            "type": "video",
            "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            "width": 480,
            "height": 270,
            "html": (
                f'<iframe src="https://www.youtube.com/embed/{video_id}" '
                'width="480" height="270"></iframe>'
            ),
        }

    @staticmethod
    def _video_id(url):
        parsed = urlparse(url)
        if parsed.netloc != "www.youtube.com" or parsed.path != "/watch":
            return None
        return parse_qs(parsed.query).get("v", [None])[0]
