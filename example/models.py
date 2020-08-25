from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet


@register_snippet
class Note(models.Model):
    text = RichTextField()
