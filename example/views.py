from django.views.generic import CreateView

from .forms import NoteForm
from .models import Note


class CreateNoteView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "example/form.html"
