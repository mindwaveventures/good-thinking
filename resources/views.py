from django.db.models import Q
from django.db import models
from django.conf import settings
import itertools
from itertools import chain
import random

from gpxpy.geo import haversine_distance

from django.http import JsonResponse, HttpResponse, Http404

import urllib.request
import os
import json

from resources.models.tags import IssueTag, ReasonTag, ContentTag
from resources.models.helpers import (
    count_likes, filter_tags,
    get_tags, base_context
)

from django.core import serializers
from django.template import loader
from django.template.loader import render_to_string

from django.apps import apps

from urllib.parse import parse_qs

from django.core.paginator import Paginator

import requests

e24_url = settings.E24_URL


def get_location(request):
    google_maps_key = os.environ.get('GOOGLE_MAPS_KEY')
    latlng = request.path.split('/location/')[1]
    url_root = "https://maps.googleapis.com/maps/api/geocode/json?"
    res = urllib.request.urlopen(
        url_root + "latlng=%s&key=%s" % (latlng, google_maps_key)
    ).read()
    address = json.loads(res)['results'][0]['address_components']
    zipcode = address[len(address) - 1]['long_name']
    # zipcode to be returned to be set as a session cookie on the client side
    return HttpResponse(zipcode)


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
                {'page': r, 'selected_tags': data['selected_tags']},
                request=request
            ),
            data['resources']
        )
    )
    mobile_resources = list(
        map(
            lambda r: render_to_string(
                'resources/short_resource_mobile.html',
                {'page': r, 'selected_tags': data['selected_tags']},
                request=request
            ),
            data['mobile_resources']
        )
    )
    json_data['resources'] = resources
    json_data['mobile_resources'] = mobile_resources

    for d in data:
        if d != 'resources' and d != 'mobile_resources':
            try:
                json_data[d] = serializers.serialize('json', data[d])
            except:
                json_data[d] = data[d]

    return JsonResponse(json_data)


def get_data(request, **kwargs):
    ResourcePage = apps.get_model('resources', 'resourcepage')
    Tip = apps.get_model('resources', 'tip')
    Assessment = apps.get_model('resources', 'assessment')
    ResourceCollections = apps.get_model('resources', 'ResourceCollections')

    data = kwargs.get('data', {})
    slug = kwargs.get('slug')
    query = request.GET.get('q')
    Home = apps.get_model('resources', 'home')

    tag_filter = request.GET.getlist('tag')
    # issue_filter = kwargs.get('path_components', request.GET.getlist('q1'))
    issue_filter = request.GET.getlist('q1')
    content_filter = request.GET.getlist('q3')
    reason_filter = request.GET.getlist('q2')
    topic_filter = request.GET.getlist('topic')
    collection_filter = kwargs.get('collection_slug')
    if request.GET.get('resource_id'):
        splited_resource = request.GET.get('resource_id').split(",")
        iapt_id_check = request.GET.get('resource_id').split(",")
        resource_id = filter(lambda id: id != "", splited_resource)
        request.session['removed_resources'] = splited_resource
    elif 'removed_resources' in request.session:
        resource_id = request.session['removed_resources']
        iapt_id_check = request.session['removed_resources']
    else:
        resource_id = []
        iapt_id_check = []

    if request.GET.get('order'):
        resource_order = request.GET.get('order')
    else:
        resource_order = "default"

    if slug != 'home':
        topic_filter = slug

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

    resources = ResourcePage.objects.all().defer(
        'background_color', 'brand_logo_id', 'brand_text',
        'hero_image_id', 'text_color'
    ).annotate(
        score=(count_likes(1) - count_likes(-1))
    ).live()

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

    tips = filter_resources(
        Tip.objects.all(),
        tag_filter=tag_filter,
        issue_filter=issue_filter,
        topic_filter=topic_filter,
        query=query
    )

    assessments = filter_resources(
        Assessment.objects.all(),
        tag_filter=tag_filter,
        issue_filter=issue_filter,
        topic_filter=topic_filter,
        query=query
    )

    top_collections = filter_resources(
        ResourceCollections.objects.all().live(),
        topic_filter=topic_filter,
    )

    iapt_resources = filter_resources(
        resources,
        topic_filter='iapt',
    )

    if iapt_resources:
        for i_id in iapt_resources.values('id'):
            for id in i_id.values():
                iapt_id = str(id)

    collection_resources =  ResourceCollections.objects.filter(Q(slug=collection_filter))

    resources = filter_resources(
        resources,
        tag_filter=tag_filter,
        issue_filter=issue_filter,
        topic_filter=topic_filter,
        query=query
    ).filter(~Q(page_ptr_id__in=list(
        chain(tips, assessments, top_collections,iapt_resources)))
    ).filter(~Q(slug="results")
    ).filter(~Q(slug="collections")
    ).filter(~Q(id__in=resource_id)
    ).prefetch_related(
        'badges'
    ).prefetch_related(
        'tagged_content_items__tag'
    ).prefetch_related(
        'tagged_reason_items__tag'
    ).prefetch_related('tagged_issue_items__tag')

    if resource_order == 'recommended':
        sorted_resources = sorted(
            resources, key=lambda resource: (
                resource.number_of_likes - resource.number_of_dislikes
            ), reverse=True
        )
    else:
        relevant_resources = map(
            lambda el: get_relevance(el, selected_tags),
            resources
        )

        # sorted_resources = sorted(
        #     relevant_resources, key=lambda resource: (
        #         resource.relevance
        #     ), reverse=True
        # )
        
        sorted_resources = sorted(
            relevant_resources, key=lambda k: random.random()
        )

    paged_resources = get_paged_resources(request, sorted_resources)

    if resources.count() == 0 and kwargs.get('path_components'):
        raise Http404()

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

    filtered_resources = map(
        lambda el: add_near(request, el),
        paged_resources
    )

    data['landing_pages'] = Home.objects.filter(~Q(slug="home")).live()
    data['resources'] = filtered_resources
    if iapt_resources:
        if iapt_id in iapt_id_check:
            sliced_resources = itertools.islice(filtered_resources, 5)
        else:
            split1_resources = itertools.islice(filtered_resources, 2)
            split2_resources = itertools.islice(filtered_resources, 2,4)
            sliced_resources=itertools.chain(split1_resources,iapt_resources,split2_resources)
    else:
        sliced_resources = itertools.islice(filtered_resources, 5)
    data['resources'],data['mobile_resources'] = itertools.tee(sliced_resources, 2)
    data['tips'] = tips
    data['assessments'] = assessments
    # data['resource_count'] = resources.count() + tips.count()
    data['resource_count'] = resources.count()
    data['selected_topic'] = topic_filter
    data['selected_tags'] = selected_tags
    data['current_page'] = slug
    data['top_collections'] = top_collections
    data['collection_resources'] = collection_resources
    data['result_block'] = Home.objects.filter(Q(slug=slug))

    return data


def get_relevance(resource, selected_tags):
    matching_content_tags = get_common_count(
        resource.content_tags.values_list('name', flat=True), selected_tags
    )
    matching_reason_tags = get_common_count(
        resource.reason_tags.values_list('name', flat=True), selected_tags
    )
    matching_issue_tags = get_common_count(
        resource.issue_tags.values_list('name', flat=True), selected_tags
    )

    resource.relevance = (
        matching_content_tags + matching_reason_tags + matching_issue_tags
    )

    return resource


def get_common_count(a, b):
    return len(set(a) - (set(a) - set(b)))


def add_near(request, el):
    if 'ldmw_location_latlong' in request.COOKIES:
        try:
            location = request.COOKIES['ldmw_location_latlong']
            [user_lat, user_long] = location.split(",")
            latlong = el.specific.latlong.values('latitude', 'longitude')
            el.specific.is_near = any(
                filter(
                    lambda e: within_mile(e, user_lat, user_long),
                    latlong
                )
            )
        except:
            print("Failed to get location")
            el.specific.is_near = False
    else:
        el.specific.is_near = False
    return el


def within_mile(resource, user_lat, user_long):
    dist = haversine_distance(
        float(user_lat), float(user_long),
        float(resource.latitude), float(resource.longitude)
    )
    return dist / 1.6 < 1000


def get_visited_resources(**kwargs):
    ResourcePage = apps.get_model('resources', 'resourcepage')
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


def filter_resources(resources, **kwargs):
    tag_filter = kwargs.get('data')
    issue_filter = kwargs.get('issue_filter')
    topic_filter = kwargs.get('topic_filter')
    query = kwargs.get('query')

    if (tag_filter):
        resources = resources.filter(
            Q(content_tags__name__in=tag_filter) |
            Q(reason_tags__name__in=tag_filter) |
            Q(issue_tags__name__in=tag_filter) |
            Q(topic_tags__name__in=tag_filter)
        ).distinct()

    if (issue_filter):
        resources = resources.filter(
            issue_tags__name__iregex=r'(' + '|'.join(issue_filter) + ')'
        ).distinct()

    if (topic_filter):
        resources = resources\
            .filter(topic_tags__name=topic_filter)\
            .distinct()

    if (query):
        resources = resources.search(query)

    return resources


def assessment_controller(self, request, **kwargs):
    ResourcePage = apps.get_model('resources', 'resourcepage')
    params = request.POST

    answers = filter(lambda p: p[:2] == "Q_", params)

    prms = {}

    for a in answers:
        if len(a.split("_")) == 3:
            prms[a.split("_")[2]] = params.get(a)
        else:
            prms[params.get(a)] = ""

    if not (params.get("member_id") and params.get("traversal_id")):
        r = requests.get(f"{e24_url}/Member?callback=raw&@usertype=300")

        response = r.json()
        member_id = response["Table"][0]["MemberID"]
        traversal_id = response["Table"][0]["TraversalID"]
    else:
        member_id = params.get("member_id")
        traversal_id = params.get("traversal_id")

    algo_id = self.algorithm_id
    node_id = 0

    node_type_id = None
    asset_id = None

    if params.get("node_id"):
        node_id = params.get("node_id")

    if params.get("algo_id"):
        algo_id = params.get("algo_id")

    if params.get("previous"):
        direction = params.get("previous")
    elif params.get("q_info"):
        direction = "Rerender"
        node_type_id = 32
        asset_id = params.get("q_info")
    elif params.get("a_info"):
        direction = "Rerender"
        node_type_id = 64
        asset_id = params.get("a_info")
    elif params.get("return_summary"):
        direction = params.get("return_summary")
    else:
        direction = "Next"

    url = f"{e24_url}/" \
        + f"{direction}/{traversal_id}/{member_id}/" \
        + f"{algo_id}/{node_id}?callback=raw"

    for p in prms:
        url += f"&{p}={prms[p]}"

    r2 = requests.get(url)

    template = loader.get_template(
        "resources/assessment/server-assessment.html"
    )

    context = r2.json()

    try:
        tags = context["Report"]["DispositionProperties"]["Tags"]
        resources = ResourcePage.objects.filter(
            hidden_tags__name__in=tags
        ).filter(
            topic_tags__name__in=self.topic_tags.names()
        )
    except:
        resources = []

    context["member_id"] = member_id
    context["traversal_id"] = traversal_id
    context["first_question"] = (node_id == 0)

    context["node_type_id"] = node_type_id
    context["asset_id"] = asset_id

    try:
        context['parent'] = self.get_parent().slug
        context['slug'] = self.slug
    except:
        context['parent'] = None
        context['slug'] = None

    context['resource_text'] = self.resource_text
    context['resources'] = resources
    context['heading'] = self.heading
    context['body'] = self.body
    context['finish_destination'] = "/"

    page = {}
    page['hero_image'] = self.hero_image
    page['header'] = self.title
    page['body'] = self.heading

    context['page'] = page


    if (self.seo_title):
        context['page_title'] = (
            self.seo_title + " | " + self.get_site().site_name
        )
    else:
        context['page_title'] = self.get_site().site_name

    if params.get("q_info") or params.get("a_info"):
        context["info"] = requests.get(
            f"{e24_url}/Info/"
            + f"{traversal_id}/{member_id}?callback=raw&@NodeTypeID="
            + f"{node_type_id}&@AssetID={asset_id}"
        ).json()

    return HttpResponse(
        template.render(context=base_context(context, self), request=request)
    )


def assessment_summary_controller(request, **kwargs):
    template = loader.get_template(
        "resources/assessment/assessment-summary.html"
    )

    traversal_id = request.POST.get("traversal_id")
    member_id = request.POST.get("member_id")

    context = requests.get(
        f"{e24_url}/Summary/"
        + f"{traversal_id}/{member_id}?callback=raw"
    ).json()

    context["member_id"] = member_id
    context["traversal_id"] = traversal_id
    context["node_id"] = request.POST.get("node_id")
    context["algo_id"] = request.POST.get("algo_id")
    context["parent"] = request.POST.get("parent")
    context["slug"] = request.POST.get("slug")

    return HttpResponse(
        template.render(context=base_context(context, self), request=request)
    )
