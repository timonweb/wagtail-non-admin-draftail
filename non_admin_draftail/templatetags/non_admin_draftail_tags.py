from django import template

register = template.Library()


@register.inclusion_tag(filename='non_admin_draftail/tags/non_admin_draftail_strings.html')
def non_admin_draftail_strings():
    return {}
