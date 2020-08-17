from django.urls import path

from non_admin_draftail.views import embed_upload_view

app_name = 'non_admin_draftail'

urlpatterns = [
    path('embed-upload/', embed_upload_view, name="embed-upload"),
]
