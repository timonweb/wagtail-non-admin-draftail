from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import NoteForm
from .models import Note


class CreateNoteView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "wagtail_non_admin_draftail_test/form.html"
    success_url = reverse_lazy("form")
