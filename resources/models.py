from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import TextField, URLField, IntegerField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class CategoryTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_items')

class AudienceTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_audience_items')

class ContentTag(TaggedItemBase):
    content_object = ParentalKey('resources.ResourcePage', related_name='tagged_content_items')

class ResourcePage(Page):
    heading = TextField(blank=True, help_text="The title of the resource being linked to")
    resource_url = URLField(blank=True, help_text="The url of the resource to link to")
    body = RichTextField(blank=True, help_text="A description of the resource")

    tags = ClusterTaggableManager(
        through=CategoryTag, blank=True,
        verbose_name='Main Tags', related_name='resource_main_tags',
        help_text='Category tags, eg: "insomnia", "fatigue", "snoring"'
    )
    audience_tags = ClusterTaggableManager(
        through=AudienceTag, blank=True,
        verbose_name='Audience Tags', related_name='resource_audience_tags',
        help_text='Audience tags, eg: "male", "female", "shiftworkers"'
    )
    content_tags = ClusterTaggableManager(
        through=ContentTag, blank=True,
        verbose_name='Content Tags', related_name='resource_content_tags',
        help_text='Content Type tags, eg: "videos", "blogs", "free", "subscription"'
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

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('resource_url', classname="full"),
        FieldPanel('body', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        FieldPanel('audience_tags'),
        FieldPanel('content_tags'),
        FieldPanel('priority'),
    ]

    class Meta:
        verbose_name = "Resource"
