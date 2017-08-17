from __future__ import unicode_literals

from django.db.models.fields import TextField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class CategoryTag(TaggedItemBase):
    content_object = ParentalKey(
        'articles.ArticlePage',
        related_name='article_tagged_items'
    )


class AudienceTag(TaggedItemBase):
    content_object = ParentalKey(
        'articles.ArticlePage',
        related_name='article_tagged_audience_items'
    )


class ContentTag(TaggedItemBase):
    content_object = ParentalKey(
        'articles.ArticlePage',
        related_name='article_tagged_content_items'
    )


class ArticlePage(Page):
    heading = TextField(blank=True, help_text="The title of the article")
    body = RichTextField(blank=True, help_text="The body text of the article")
    tags = ClusterTaggableManager(
        through=CategoryTag, blank=True,
        verbose_name='Main Tags', related_name='article_main_tags',
        help_text='Category tags, eg: "insomnia", "fatigue", "snoring"'
    )
    audience_tags = ClusterTaggableManager(
        through=AudienceTag, blank=True,
        verbose_name='Audience Tags', related_name='article_audience_tags',
        help_text='Audience tags, eg: "male", "female", "shiftworkers"'
    )
    content_tags = ClusterTaggableManager(
        through=ContentTag, blank=True,
        verbose_name='Content Tags', related_name='article_content_tags',
        help_text='Content Type tags, eg: "videos", "blogs", "free"'
    )

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('body', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        FieldPanel('audience_tags'),
        FieldPanel('content_tags'),
    ]

    class Meta:
        verbose_name = "Article"
