from django.urls import path
from .views import CreateNoteView

app_name = "example"

urlpatterns = [
    path("form/", CreateNoteView.as_view(), name='form'),
]
