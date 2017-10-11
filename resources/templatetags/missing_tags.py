from django import template

register = template.Library()


@register.filter
def missing_tags(selected, page):
    return list(filter(
        lambda s: s not in
        page.content_tags.values_list('name', flat=True) +
        page.reason_tags.values_list('name', flat=True) +
        page.issue_tags.values_list('name', flat=True),
        selected
    ))
