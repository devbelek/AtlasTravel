from django import template
from jazzmin.templatetags import jazzmin

register = template.Library()


@register.simple_tag(takes_context=True)
def safe_sidebar_status(context):
    request = context.get('request')
    if not request or not hasattr(request, 'COOKIES'):
        return ""
    try:
        return jazzmin.sidebar_status(context)
    except AttributeError:
        return ""