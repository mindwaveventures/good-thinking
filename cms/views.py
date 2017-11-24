from django.template import Template, Context, RequestContext, loader
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from resources.models.helpers import base_context

from wagtail.wagtaildocs.models import Document


def robots_handler(request):
    document = get_object_or_404(Document, title="robots.txt")
    content = document.file.read()
    template = Template(content)

    return HttpResponse(
        template.render(Context({})),
        content_type="text/plain"
    )


def not_found_handler(request):
    t = loader.get_template('404.html')

    return HttpResponseNotFound(
        t.render(
            RequestContext(
                request,
                base_context({})
            )
        )
    )
