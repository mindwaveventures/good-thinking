from django import template

register = template.Library()


@register.filter
def split_list(value, arg):
    for i in range(0, len(value), arg):
        yield value[i:i + arg]
