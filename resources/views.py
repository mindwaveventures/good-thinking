from django.db.models import Q

from itertools import chain

from django.http import JsonResponse

from resources.models.tags import TopicTag, IssueTag, ReasonTag, ContentTag
from resources.models.resources import ResourcePage
from resources.models.helpers import (
    combine_tags, count_likes, filter_tags,
    get_tags, get_order, get_relevance
)

from django.core import serializers
from django.template.loader import render_to_string

from django.apps import apps


def get_json_data(request):
    data = get_data(request)
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

    resources = get_order(ResourcePage.objects.all().annotate(
        number_of_likes=count_likes(1),
        number_of_dislikes=count_likes(-1),
        score=(count_likes(1) - count_likes(-1)),
        relevance=(get_relevance(selected_tags))
    ), resource_order)

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

    filtered_resources = map(combine_tags, resources)

    data['landing_pages'] = Home.objects.filter(~Q(slug="home"))
    data['resources'] = filtered_resources
    data['resource_count'] = resources.count()
    data['topic_tags'] = topic_tags.values()
    data['selected_topic'] = topic_filter
    data['selected_tags'] = selected_tags

    return data
