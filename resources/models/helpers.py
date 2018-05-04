from django.db import models
from django.db.models import Case, When, Count, Q

from taggit.models import Tag
from itertools import chain

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

    exclude = chain(exclude_tags, topic_tag)

    issue_tags = filter_resource_by_topic(resources, IssueTag, exclude)
    reason_tags = filter_resource_by_topic(resources, ReasonTag, exclude)
    content_tags = filter_resource_by_topic(resources, ContentTag, exclude)

    return issue_tags, reason_tags, content_tags


def filter_resource_by_topic(resource_ids, tag_type, exclude):
    return tag_type.objects.filter(content_object__in=resource_ids).exclude(
        tag__in=exclude
    )


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


def base_context(context,self):
    Main = apps.get_model('resources', 'main')
    HomeSiteMap = apps.get_model('resources', 'homesitemap')
    HomeFooterLinks = apps.get_model('resources', 'homefooterlinks')
    HomeFooterBlocks = apps.get_model('resources', 'homefooterblocks')
    Home = apps.get_model('resources', 'home')
    HomeCollections = apps.get_model('resources', 'homecollections')
    HomeHighLightsOfMonth = apps.get_model('resources', 'homehighlightsofmonth')
    ResourcePageSelectResources = apps.get_model('resources', 'resourcepageselectresources')
    ResourcePage = apps.get_model('resources', 'resourcepage')
    home_page = Main.objects.get(slug="home")
    banner = {}
    banner['text'] = home_page.banner
    banner['button_1_text'] = home_page.banner_button_1_text
    banner['button_1_link'] = home_page.banner_button_1_link
    banner['button_2_text'] = home_page.banner_button_2_text
    banner['button_2_link'] = home_page.banner_button_2_link

    site_map = HomeSiteMap.objects.all().select_related('link_page')
    footer_links = HomeFooterLinks.objects.all().select_related('footer_image')
    footer_blocks = HomeFooterBlocks.objects.all().select_related('link_page')
    collections = HomeCollections.objects.filter(page_id=self.page_ptr_id)
    highlights = HomeHighLightsOfMonth.objects.all().select_related('highlights_link')
    selected_resources = ResourcePageSelectResources.objects.all().select_related('collection_resource')

    context['selected_resources'] = selected_resources
    context['collections'] = collections
    context['highlights'] = highlights
    context['banner'] = banner
    context['site_map'] = site_map
    context['footer_links'] = footer_links
    context['footer_blocks'] = footer_blocks
    context['landing_pages'] = list(
        Home.objects.filter(~Q(slug="home")).live().values()
    )

    return context
