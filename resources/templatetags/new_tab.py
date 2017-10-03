from django import template

import re

register = template.Library()


@register.filter
def new_tab(html_string):
    return re.sub(
        r'a href=\"([^\/])',
        "a target=\"_blank\" href=\"\\1",
        str(html_string)
    )
