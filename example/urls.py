from django.urls import path
from .views import form_view

app_name = "example"

urlpatterns = [
    path("form/", form_view, name='form'),
]
