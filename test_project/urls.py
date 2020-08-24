from django.urls import path, include

urlpatterns = [
    path("non-admin-draftail/", include("non_admin_draftail.urls", namespace="non_admin_draftail")),
    path("example/", include("example.urls", namespace="example"))
]
