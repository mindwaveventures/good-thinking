from django.db import models
from django.db.models import Sum, Case, When, Count, Q

from taggit.models import Tag
from itertools import chain
import threading
import queue

from resources.models.tags import ContentTag, IssueTag, ReasonTag

from django.apps import apps


def get_tags(tag_type, **kwargs):
    filtered_tags = kwargs.get('filtered_tags', tag_type.objects.values('id'))
    tag_ids = [tag.tag_id for tag in filtered_tags]
    tags = Tag.objects.in_bulk(tag_ids)

    return tags


def create_tag_combiner(exclude):
    if not exclude:
        exclude = []

    def combine_tags(element):
        element.specific.tags = filter(lambda x: x not in exclude, list(chain(
            element.specific.content_tags.all(),
            element.specific.issue_tags.all(),
            element.specific.reason_tags.all(),
        )))
        return element
    return combine_tags


def get_resource(id, user_hash):
    num_likes = 'select ' \
        + 'count(like_value) from likes_likes ' \
        + 'where resource_id = %s ' \
        + 'and like_value = %s'

    liked_value = 'select ' \
        + 'like_value from likes_likes ' \
        + 'where resource_id = %s ' \
        + 'and user_hash = %s'

    ResourcePage = apps.get_model('resources', 'resourcepage')

    combine_tags = create_tag_combiner(None)

    return combine_tags(
        ResourcePage.objects
        .extra(
            select={'number_of_likes': num_likes},
            select_params=([id, 1])
        )
        .extra(
            select={'number_of_dislikes': num_likes},
            select_params=([id, -1])
        )
        .extra(
            select={'liked_value': liked_value},
            select_params=([id, user_hash])
        )
        .get(id=id)
    )


def count_likes(like_or_dislike):
    return Count(
        Case(
            When(likes__like_value=like_or_dislike, then=1),
            output_field=models.IntegerField()
        ), distinct=True
    )


def get_liked_value(user_hash):
    return Case(
        When(likes__user_hash=user_hash, then='likes__like_value'),
        default=0,
        output_field=models.IntegerField()
    )


def filter_tags(resources, topic):
    Home = apps.get_model('resources', 'home')
    exclude_tags = Home.objects.get(slug=topic).specific.exclude_tags.all()
    topic_tag = Tag.objects.filter(name=topic)

    contains_tag_filter = makefilter(topic)

    fil = list(map(lambda r: r.id, filter(contains_tag_filter, resources)))
    q = queue.Queue()

    threads = [
        threading.Thread(
            target=filter_resource_by_topic,
            name=t,
            args=(fil, t, q)
        )
        for t in [ContentTag, IssueTag, ReasonTag]
    ]

    # Using threads to make sure all db calls
    # are completed before function returns

    for th in threads:
        th.start()

    content_tags = q.get().exclude(
        tag__in=list(chain(exclude_tags, topic_tag))
    )
    issue_tags = q.get().exclude(
        tag__in=list(chain(exclude_tags, topic_tag))
    )
    reason_tags = q.get().exclude(
        tag__in=list(chain(exclude_tags, topic_tag))
    )

    return issue_tags, reason_tags, content_tags


def makefilter(t):
    def contains_tag(r):
        return any(
            filter(lambda tag: tag.name == t, r.specific.topic_tags.all())
        )
    return contains_tag


def filter_resource_by_topic(resource_ids, tag_type, result_queue):
    result_queue.put(tag_type.objects.filter(content_object__in=resource_ids))


def valid_request(request_dict):
    # TODO: don't hardcode this, instead generate it dynamically
    # For now the cms home page cannot cater for further form elements

    return "suggestion" in request_dict \
        or "email" in request_dict \
        or "feedback" in request_dict


def handle_request(request, request_dict, cb, messages_):
    if "suggestion" in request_dict:
        messages_.info(request, 'suggestion')
        return cb(request.path + "#suggestion_form")

    if "email" in request_dict:
        messages_.info(request, 'email')
        return cb(request.path + "#alphasection")

    if "feedback" in request_dict:
        try:
            resource_id = request_dict['id'][0]
        except:
            resource_id = request_dict['id']
        messages_.info(request, 'like_feedback_' + str(resource_id))
        return cb(request.path + "#resource_" + resource_id)


def generate_custom_form(form_fields, request_dict, messages_):
    custom_form = []

    for field in form_fields:
        dict = {}
        dict['field_type'] = field.field_type
        dict['default_value'] = field.default_value
        dict['help_text'] = field.help_text
        dict['label'] = field.label

        try:
            dict['submitted_val'] = request_dict[field.label][0]
        except:
            try:
                if len(request_dict[field.label]) > 0:
                    dict['submitted_val'] = request_dict[field.label]
            except:
                dict['submitted_val'] = ''

        dict['required'] = 'required' if field.required else ''

        dict['email_submitted'] = False
        dict['suggestion_submitted'] = False

        for message in messages_:
            if message.__str__() == 'email':
                dict['email_submitted'] = True
            if message.__str__() == 'suggestion':
                dict['suggestion_submitted'] = True

        custom_form.append(dict)

    return custom_form


def get_order(resources, order):
    if order == 'recommended':
        return resources.order_by('-score')
    else:
        return resources.order_by('-relevance')


def get_relevance(selected_tags):
    if not selected_tags:
        selected_tags = [""]

    return Sum(
        Case(
            When(content_tags__name__in=selected_tags, then=1),
            When(reason_tags__name__in=selected_tags, then=1),
            default=0,
            output_field=models.IntegerField()
        )
    )


def base_context(context):
    Main = apps.get_model('resources', 'main')
    HomeFooterLinks = apps.get_model('resources', 'homefooterlinks')
    HomeFooterBlocks = apps.get_model('resources', 'homefooterblocks')
    Home = apps.get_model('resources', 'home')

    banner = Main.objects.get(slug="home").banner
    footer_links = HomeFooterLinks.objects.all()
    footer_blocks = HomeFooterBlocks.objects.all()

    context['banner'] = banner
    context['footer_links'] = footer_links
    context['footer_blocks'] = footer_blocks
    context['landing_pages'] = Home.objects.filter(~Q(slug="home")).live()

    return context
