from django.template import Template, Context
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from wagtail.wagtaildocs.models import Document


def robots_handler(request):
    document = get_object_or_404(Document, title="robots.txt")
    content = document.file.read()
    template = Template(content)

    return HttpResponse(
        template.render(Context({})),
        content_type="text/plain"
    )
