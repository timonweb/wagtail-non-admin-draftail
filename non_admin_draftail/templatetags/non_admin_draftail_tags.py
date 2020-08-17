import json

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag(filename='non_admin_draftail/tags/non_admin_draftail_strings.html')
def non_admin_draftail_strings():
    return {
        'URLS': mark_safe(json.dumps({
            'embed_upload': reverse('non_admin_draftail:embed-upload')
        }))
    }
