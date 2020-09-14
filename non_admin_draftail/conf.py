from django.conf import settings

NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME = getattr(
    settings, "NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME", "Public uploads"
)
