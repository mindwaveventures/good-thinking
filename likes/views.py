from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

import uuid

from likes.models import Likes
from resources.models.resources import ResourcePage
from resources.models.helpers import get_resource

import re


def save_like(request):
    id = request.POST.get('id')
    like_value = request.POST.get('like')
    csrf = request.POST.get('csrfmiddlewaretoken')
    uid = uuid.uuid4()

    if 'ldmw_session' in request.COOKIES:
        cookie = request.COOKIES['ldmw_session']
    else:
        cookie = uid.hex

    linked_resource = ResourcePage.objects.get(id=id)

    obj, created = Likes.objects.get_or_create(
        user_hash=cookie,
        resource=linked_resource,
        defaults={'like_value': like_value},
    )

    if not created:
        if obj.like_value == int(like_value):
            obj.delete()
        else:
            obj.like_value = like_value
            obj.save(update_fields=['like_value'])

    resource = get_resource(id, cookie)

    if re.search('/' + resource.slug + '/', request.META['HTTP_REFERER']):
        template = 'resources/resource.html'
    else:
        template = 'resources/short_resource.html'

    result = render_to_string(template, {'page': resource, 'csrf_token': csrf})

    if request.META.get('HTTP_ACCEPT') == 'application/json':
        response = JsonResponse({'result': result, 'id': id})
    else:
        response = redirect(f'/#resource_{id}')

    response.set_cookie('ldmw_session', cookie)
    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
