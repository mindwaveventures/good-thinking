from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from django.db import models
from django.db.models import Sum, Case, When
from django.db.models.fields import IntegerField

from likes.models import Likes
from resources.models import ResourcePage, combine_tags, get_resource
from django.template.loader import render_to_string

import bcrypt

def save_like(request):
    id = request.POST.get('id')
    like_value = request.POST.get('like')
    csrf = request.POST.get('csrfmiddlewaretoken')
    ip = get_client_ip(request)

    linked_resource = ResourcePage.objects.get(id=id)

    obj, created = Likes.objects.get_or_create(
        user_ip=ip,
        resource=linked_resource,
        defaults={'like_value': like_value},
    )

    if not created:
        if obj.like_value == int(like_value):
            obj.delete()
        else:
            obj.like_value = like_value
            obj.save(update_fields=['like_value'])

    resource = get_resource(like_value, id)

    result = render_to_string('resources/resource.html', {'page': resource, 'csrf_token': csrf})

    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return JsonResponse({'result':result, 'id': id})
    else:
        return redirect(f'/#resource_{id}')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
