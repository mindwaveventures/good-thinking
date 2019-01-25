from django import template
from itertools import chain

register = template.Library()


@register.filter
def missing_tags(selected, page):
    return list(filter(
        lambda s: s.lower() not in
        list(chain(
            map(
                lambda n: n.lower(),
                page.content_tags.values_list('name', flat=True)
            ),
            map(
                lambda n: n.lower(),
                page.reason_tags.values_list('name', flat=True)
            ),
            map(
                lambda n: n.lower(),
                page.issue_tags.values_list('name', flat=True)
            )
        )),
        selected
    ))
