from django import template

register = template.Library()


@register.filter
def multiline(str):
    return str.split('\n')
