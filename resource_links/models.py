from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import TextField, URLField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class ResourceLinkPageTag(TaggedItemBase):
    content_object = ParentalKey('resource_links.ResourceLinkPage', related_name='tagged_items')

class ResourceLinkPage(Page):
    heading = TextField(blank=True, help_text="The title of the resource being linked to")
    resource_url = URLField(blank=True, help_text="The url of the resource to link to")
    tags = ClusterTaggableManager(through=ResourceLinkPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('resource_url', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    class Meta:
        verbose_name = "Resource Link"
