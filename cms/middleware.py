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
        print(host)
        if host == 'localhost:8000':
            return redirect(settings.BASE_URL)
        else:
            return self.get_response(request)
