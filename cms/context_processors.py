from django.conf import settings


def add_variable_to_context(request):
    return {
        'GTM_TOKEN': settings.GTM_TOKEN
    }
