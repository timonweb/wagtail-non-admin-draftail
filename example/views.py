from django.shortcuts import render
from .forms import ExampleForm


def form_view(request):
    return render(request, "example/form.html", {
        "form": ExampleForm
    })
