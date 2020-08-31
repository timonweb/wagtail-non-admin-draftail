from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "non-admin-draftail/",
        include("non_admin_draftail.urls", namespace="non_admin_draftail"),
    ),
    path("example/", include("example.urls", namespace="example")),
    path("login/", LoginView.as_view(), name="login"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
