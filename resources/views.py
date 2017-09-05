from django.db.models import Q

from itertools import chain

import urllib.request
import os
import json

from django.http import JsonResponse, HttpResponse

from resources.models.tags import TopicTag, IssueTag, ReasonTag, ContentTag
from resources.models.resources import ResourcePage
from resources.models.helpers import (
    combine_tags, count_likes, filter_tags,
    get_tags, get_order, get_relevance
)

from django.core import serializers
from django.template.loader import render_to_string

from django.apps import apps

from urllib.parse import parse_qs

from django.core.paginator import Paginator


def get_location(request):
    google_maps_key = os.environ.get('GOOGLE_MAPS_KEY')
    latlng = request.path.split('/location/')[1]
    url_root = "https://maps.googleapis.com/maps/api/geocode/json?"
    res = urllib.request.urlopen(
        url_root + "latlng=%s&key=%s" % (latlng, google_maps_key)
    ).read()
    address = json.loads(res)['results'][0]['address_components']
    zipcode = address[len(address) - 1]['long_name']
    request.session['location'] = zipcode
    return HttpResponse('Set location session')


def get_json_data(request):
    try:
        query = request.GET.urlencode()
        slug = parse_qs(query)['slug'][0]
    except:
        slug = ''

    data = get_data(request, slug=slug)
    json_data = {}

    resources = list(
        map(
            lambda r: render_to_string(
                'resources/short_resource.html',
                {'page': r},
                request=request
            ),
            data['resources']
        )
    )

    json_data['resources'] = resources

    for d in data:
        if not d == 'resources':
            try:
                json_data[d] = serializers.serialize('json', data[d])
            except:
                json_data[d] = data[d]

    return JsonResponse(json_data)


def get_data(request, **kwargs):
    data = kwargs.get('data', {})
    slug = kwargs.get('slug')
    query = request.GET.get('q')
    Home = apps.get_model('resources', 'home')

    tag_filter = request.GET.getlist('tag')
    issue_filter = request.GET.getlist('issue')
    content_filter = request.GET.getlist('content')
    reason_filter = request.GET.getlist('reason')
    topic_filter = request.GET.getlist('topic')

    if request.GET.get('order'):
        resource_order = request.GET.get('order')
    else:
        resource_order = "default"

    if slug != 'home':
        topic_filter = slug

    issue_tags = get_tags(IssueTag)
    content_tags = get_tags(ContentTag)
    reason_tags = get_tags(ReasonTag)
    topic_tags = get_tags(TopicTag)

    selected_tags = list(chain(
        tag_filter,
        issue_filter,
        content_filter,
        reason_filter,
    ))

    num_likes = 'select ' \
        + 'count(like_value) from likes_likes ' \
        + 'where resource_id = resources_resourcepage.page_ptr_id ' \
        + 'and like_value = %s'

    resources = get_order(ResourcePage.objects.all().annotate(
        score=(count_likes(1) - count_likes(-1)),
        relevance=(get_relevance(selected_tags))
    ), resource_order).live()

    resources = resources.extra(
        select={'number_of_likes': num_likes},
        select_params=([1])
    )

    resources = resources.extra(
        select={'number_of_dislikes': num_likes},
        select_params=([-1])
    )

    if 'ldmw_session' in request.COOKIES:
        cookie = request.COOKIES['ldmw_session']
        liked_value = 'select ' \
            + 'like_value from likes_likes where ' \
            + 'resource_id  = resources_resourcepage.page_ptr_id '\
            + 'and user_hash = %s'
        resources = resources.extra(
            select={'liked_value': liked_value},
            select_params=([cookie])
        )
    else:
        cookie = ''

    if 'ldmw_visited_resources' in request.COOKIES:
        data['visited'] = get_visited_resources(
            visited_cookie=request.COOKIES['ldmw_visited_resources'],
            user_cookie=cookie
        )

    if topic_filter:
        (
            filtered_issue_tags,
            filtered_reason_tags,
            filtered_content_tags,
        ) = filter_tags(resources, topic_filter)

        if filtered_issue_tags:
            data['issue_tags'] = get_tags(
                IssueTag,
                filtered_tags=filtered_issue_tags
            ).values()

        if filtered_content_tags:
            data['content_tags'] = get_tags(
                ContentTag,
                filtered_tags=filtered_content_tags
            ).values()

        if filtered_reason_tags:
            data['reason_tags'] = get_tags(
                ReasonTag,
                filtered_tags=filtered_reason_tags
            ).values()
    else:
        data['issue_tags'] = issue_tags.values()
        data['content_tags'] = content_tags.values()
        data['reason_tags'] = reason_tags.values()

    if (tag_filter):
        resources = resources.filter(
            Q(content_tags__name__in=tag_filter) |
            Q(reason_tags__name__in=tag_filter) |
            Q(issue_tags__name__in=tag_filter) |
            Q(topic_tags__name__in=tag_filter)
        ).distinct()

    if (issue_filter):
        resources = resources\
            .filter(issue_tags__name__in=issue_filter)\
            .distinct()

    if (topic_filter):
        resources = resources\
            .filter(topic_tags__name=topic_filter)\
            .distinct()

    if (query):
        resources = resources.search(query)

    paged_resources = get_paged_resources(request, resources)

    filtered_resources = map(combine_tags, paged_resources)

    data['landing_pages'] = Home.objects.filter(~Q(slug="home")).live()
    data['resources'] = filtered_resources
    data['resource_count'] = resources.count()
    data['topic_tags'] = topic_tags.values()
    data['selected_topic'] = topic_filter
    data['selected_tags'] = selected_tags

    return data


def get_visited_resources(**kwargs):
    visited_cookie = kwargs.get('visited_cookie')
    user_cookie = kwargs.get('user_cookie')

    if visited_cookie:
        visited_ids = filter(lambda x: x != "", visited_cookie.split(','))
    else:
        visited_ids = []

    liked_value = """select like_value from likes_likes
    where resource_id = resources_resourcepage.page_ptr_id
    and user_hash = %s"""
    visited_resources = ResourcePage.objects\
        .filter(id__in=visited_ids)\
        .extra(
          select={'liked_value': liked_value},
          select_params=([user_cookie])
        )

    return visited_resources


def get_paged_resources(request, resources):
    paginator = Paginator(resources, 3)

    try:
        if request.GET.get('page') == 'initial':
            paged_resources = paginator.page(1)
        elif request.GET.get('page') == 'remainder':
            try:
                current_page = paginator.page(2)
                paged_resources = chain(current_page)

                while current_page.has_next():
                    current_page = paginator.page(
                        current_page.next_page_number()
                    )
                    paged_resources = chain(paged_resources, current_page)
            except:
                paged_resources = []
        else:
            paged_resources = resources
    except:
        paged_resources = resources

    return paged_resources
