from __future__ import unicode_literals

from django.db import models
from django.db.models import Q, Sum, Case, When
from django.db.models.fields import TextField, URLField, IntegerField, CharField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag
from wagtail.wagtailsearch import index

from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.template.loader import get_template

from itertools import chain

from likes.models import Likes

class Home(Page):
    banner = RichTextField(blank=True, help_text="Banner at the top of every page")
    header = RichTextField(blank=True, help_text="Hero title")
    body = RichTextField(blank=True, help_text="Description of page")
    filter_label_1 = TextField(blank=True, help_text="Label/Question for first set of filters")
    filter_label_2 = TextField(blank=True, help_text="Label/Question for second set of filters")
    filter_label_3 = TextField(blank=True, help_text="Label/Question for third set of filters")
    assessment_text = RichTextField(blank=True, help_text="Label for sleep assessment link")
    crisis_text = RichTextField(blank=True, help_text="Label for sleep crisis page link")
    lookingfor = RichTextField(blank=True, help_text="Information on how to leave suggestions and what the suggestions are for")
    alpha = RichTextField(blank=True, help_text="What is Alpha")
    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")
    footer = RichTextField(blank=True, help_text="Footer text")
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Max file size: 10MB. Choose from: GIF, JPEG, PNG (but pick PNG if you have the choice)"
    )
    video_url = URLField(blank=True, help_text="URL of an introductiary youtube video")

    def get_context(self, request):
        context = super(Home, self).get_context(request)

        query = request.GET.get('q')

        tag_filter = request.GET.getlist('tag')
        issue_filter = request.GET.getlist('issue')
        content_filter = request.GET.getlist('content')
        reason_filter = request.GET.getlist('reason')
        topic_filter = request.GET.getlist('topic')

        issue_tags = get_tags(IssueTag)
        content_tags = get_tags(ContentTag)
        reason_tags = get_tags(ReasonTag)
        topic_tags = get_tags(TopicTag)

        if 'ldmw_session' in request.COOKIES:
            cookie = request.COOKIES['ldmw_session']
        else:
            cookie = ''

        resources = ResourcePage.objects.all().annotate(
            number_of_likes=count_likes(1)
        ).annotate(
            number_of_dislikes=count_likes(-1)
        )

        if 'ldmw_session' in request.COOKIES:
            resources = resources.annotate(
                liked_value=get_liked_value(request.COOKIES['ldmw_session'])
            )

        if (tag_filter):
            resources = resources.filter(
                Q(content_tags__name__in=tag_filter) |
                Q(reason_tags__name__in=tag_filter) |
                Q(issue_tags__name__in=tag_filter) |
                Q(topic_tags__name__in=tag_filter)
            ).distinct()

        if (issue_filter):
            resources = resources.filter(issue_tags__name__in=issue_filter).distinct()

        if (content_filter):
            resources = resources.filter(content_tags__name__in=content_filter).distinct()

        if (reason_filter):
            resources = resources.filter(reason_tags__name__in=reason_filter).distinct()

        if (topic_filter):
            resources = resources.filter(topic_tags__name__in=topic_filter).distinct()

        if (query):
            resources = resources.search(query)

        filtered_resources = map(combine_tags, resources)

        context['resources'] = filtered_resources
        context['resource_count'] = resources.count()
        context['issue_tags'] = issue_tags.values()
        context['content_tags'] = content_tags.values()
        context['reason_tags'] = reason_tags.values()
        context['topic_tags'] = topic_tags.values()
        context['selected_topic'] = topic_filter
        context['selected_tags'] = list(chain(
            tag_filter,
            issue_filter,
            content_filter,
            reason_filter,
            topic_filter,
        ))
        return context

    content_panels = Page.content_panels + [
        FieldPanel('banner', classname="full"),
        ImageChooserPanel('hero_image'),
        FieldPanel('header', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('video_url', classname="full"),
        FieldPanel('filter_label_1', classname="full"),
        FieldPanel('filter_label_2', classname="full"),
        FieldPanel('filter_label_3', classname="full"),
        FieldPanel('assessment_text', classname="full"),
        FieldPanel('crisis_text', classname="full"),
        FieldPanel('lookingfor', classname="full"),
        FieldPanel('alpha', classname="full"),
        FieldPanel('alphatext', classname="full"),
        FieldPanel('footer', classname="full"),
    ]

class TopicTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_topic_items')

class IssueTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_issue_items')

class ReasonTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_reason_items')

class ContentTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_content_items')

class HiddenTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_hidden_items')

class ResourceIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super(ResourceIndexPage, self).get_context(request)
        resources = self.get_children().live().order_by('-first_published_at')
        context['resources'] = resources
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class ResourcePage(Page):
    heading = TextField(blank=True, help_text="The title of the resource being linked to")
    resource_url = URLField(blank=True, help_text="The url of the resource to link to")
    body = RichTextField(blank=True, help_text="A description of the resource")
    pros = RichTextField(blank=True, help_text="A list of pros for the resource")
    cons = RichTextField(blank=True, help_text="A list of cons for the resource")
    video_url = URLField(blank=True, help_text="URL of a youtube video for the resource")

    topic_tags = ClusterTaggableManager(
        through=TopicTag, blank=True,
        verbose_name='Topic Tags', related_name='resource_topic_tags',
        help_text='Topic tags, eg: "sleep", "depression", "stress"'
    )
    issue_tags = ClusterTaggableManager(
        through=IssueTag, blank=True,
        verbose_name='Issue Tags', related_name='resource_issue_tags',
        help_text='Issue tags, eg: "insomnia", "fatigue", "snoring"'
    )
    reason_tags = ClusterTaggableManager(
        through=ReasonTag, blank=True,
        verbose_name='Reason Tags', related_name='resource_reason_tags',
        help_text='Reason tags, eg: "loneliness", "relationships"'
    )
    content_tags = ClusterTaggableManager(
        through=ContentTag, blank=True,
        verbose_name='Content Tags', related_name='resource_content_tags',
        help_text='Content Type tags, eg: "videos", "blogs", "free", "subscription"'
    )
    hidden_tags = ClusterTaggableManager(
        through=HiddenTag, blank=True,
        verbose_name='Hidden Tags', related_name='resource_hidden_tags',
        help_text='Hidden tags for admin use'
    )
    PRIORITY_CHOICES = (
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
    )
    priority = IntegerField(
      choices=PRIORITY_CHOICES,
      default='5',
      help_text='Highest priority 1, lowest priority 5'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('pros'),
        index.SearchField('cons'),
        index.SearchField('heading'),
        index.SearchField('resource_url'),
        index.RelatedFields('issue_tags', [
            index.SearchField('name'),
        ]),
        index.RelatedFields('content_tags', [
            index.SearchField('name'),
        ]),
        index.RelatedFields('reason_tags', [
            index.SearchField('name'),
        ]),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('resource_url', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('pros', classname="full"),
        FieldPanel('cons', classname="full"),
        FieldPanel('video_url', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('topic_tags'),
        FieldPanel('issue_tags'),
        FieldPanel('reason_tags'),
        FieldPanel('content_tags'),
        FieldPanel('hidden_tags'),
        FieldPanel('priority'),
    ]

    class Meta:
        verbose_name = "Resource"

def get_tags(tag_type):
    tag_ids = [tag.tag_id for tag in tag_type.objects.all()]
    tags = Tag.objects.in_bulk(tag_ids)

    return tags

def combine_tags(element):
    element.specific.tags = list(chain(
        element.specific.content_tags.all(),
        element.specific.issue_tags.all(),
        element.specific.reason_tags.all(),
        element.specific.topic_tags.all()
    ))
    return element

def get_resource(id, user_hash):
    return combine_tags(
        ResourcePage.objects
        .annotate(number_of_likes=count_likes(1))
        .annotate(number_of_dislikes=count_likes(-1))
        .annotate(liked_value=get_liked_value(user_hash))
        .get(id=id)
    )

def count_likes(like_or_dislike):
    return Sum(
        Case(
            When(likes__like_value=like_or_dislike, then=1),
            default=0,
            output_field=models.IntegerField()
        )
    )

def get_liked_value(user_hash):
    return Case(
        When(likes__user_hash=user_hash, then='likes__like_value'),
        default=0,
        output_field=models.IntegerField()
    )
