from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def app_is_installed(app_name):
    return apps.is_installed(app_name)
