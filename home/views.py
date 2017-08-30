from django.template import loader
from django.http import HttpResponse


def landing_page_controller(request, **kwargs):
    split_path = request.get_full_path().split('/')

    path = '-'.join(filter(lambda e: e != '', split_path))

    template = loader.get_template(f"home/{path}.html")

    return HttpResponse(template.render(context=None, request=request))
