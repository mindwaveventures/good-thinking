from django import template

register = template.Library()


@register.filter
def continue_reading(text, obj):
    return text + ' ' \
        + f'<a class="lm-dark-turquoise lm-pink-hover ' \
        + 'link" href="/{obj.parent}' \
        + '/' + f'{obj.slug}">continue reading</a>'
