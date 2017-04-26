from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('articles.ArticlePage', related_name='tagged_items')

class ArticlePage(Page):
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

