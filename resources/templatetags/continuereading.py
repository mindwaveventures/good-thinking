from django import template

register = template.Library()


@register.filter
def continue_reading(text, obj):
    return text + ' ' \
        + '<a class="lm-dark-turquoise lm-pink-hover ' \
        + f'link" href="/{obj.parent}' \
        + '/' + f'{obj.slug}">continue reading</a>'
