from django import template

import re

register = template.Library()


@register.filter
def continue_reading(text, obj):
    # Finds last closing html tag and inserts link before it
    cont = re.sub(
        r'(<\/[^>]+>)$',
        ' <a class="lm-dark-turquoise lm-pink-hover '
        + f'link" href="/{obj.parent}'
        + f'/{obj.slug}">continue reading</a>\\1',
        text
    )

    return cont
