from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("non-admin-draftail/", include("non_admin_draftail.urls", namespace="non_admin_draftail")),
    path("example/", include("example.urls", namespace="example"))
]
