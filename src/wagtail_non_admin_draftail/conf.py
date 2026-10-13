from django.conf import settings

WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME = getattr(
    settings, "WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME", "Public uploads"
)
