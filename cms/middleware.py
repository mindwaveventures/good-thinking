from django.shortcuts import redirect
from django.conf import settings


class RedirectFromLMMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            host = request.META['HTTP_HOST']
        except:
            host = ''

        if host in settings.REDIRECT_FROM:
            return redirect(settings.BASE_URL + request.path, permanent=True)
        else:
            return self.get_response(request)
