from django.db import models
from django.urls import reverse
from wagtail.fields import RichTextField


class Note(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:detail", args=[self.pk])
