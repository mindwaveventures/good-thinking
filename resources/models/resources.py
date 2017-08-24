from wagtail.wagtailforms.models import AbstractForm, Page, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel
)
from wagtail.wagtailsearch import index

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from django.db.models.fields import TextField, URLField, IntegerField
from django.apps import apps
from django.db.models import Q
from django.db import models

from colorful.fields import RGBColorField

from resources.models.tags import (
    TopicTag, IssueTag, ReasonTag,
    ContentTag, HiddenTag
)

from likes.models import Likes

from resources.models.helpers import combine_tags


class ResourceFormField(AbstractFormField):
    page = ParentalKey('ResourceIndexPage', related_name='form_fields')


class ResourceIndexPage(AbstractForm):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super(ResourceIndexPage, self).get_context(request)
        resources = self.get_children().live().order_by('-first_published_at')
        context['resources'] = resources
        return context

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
    ]


class ResourcePage(Page):
    heading = TextField(
        blank=True,
        help_text="The title of the resource being linked to"
    )
    resource_url = URLField(
        blank=True,
        help_text="The url of the resource to link to"
    )
    body = RichTextField(
        blank=True,
        help_text="A description of the resource"
    )
    pros = RichTextField(
        blank=True,
        help_text="A list of pros for the resource"
    )
    cons = RichTextField(
        blank=True,
        help_text="A list of cons for the resource"
    )
    video_url = URLField(
        blank=True,
        help_text="URL of a youtube video for the resource"
    )

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
        help_text="""
            Content Type tags, eg: "videos", "blogs", "free", "subscription"
        """
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

    background_color = RGBColorField(
        default='#ffffff', null=True, blank=True,
        help_text="The background colour to use if there is no hero image"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="""
            Max file size: 10MB. Choose from: GIF, JPEG, PNG
            (but pick PNG if you have the choice)
        """
    )
    brand_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="""
            Max file size: 10MB. Choose from: GIF, JPEG, PNG
            (but pick PNG if you have the choice)
        """
    )
    brand_text = RichTextField(blank=True)
    text_color = RGBColorField(
        default='#000000', null=True, blank=True,
        help_text="""
            The colour of the brand text.
            It should contrast well with the background colour or image
        """
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
        MultiFieldPanel([
            ImageChooserPanel('hero_image'),
            FieldPanel('background_color'),
            ImageChooserPanel('brand_logo'),
            FieldPanel('brand_text'),
            FieldPanel('text_color')
        ], heading="Branding"),
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

    def __init__(self, *args, **kwargs):
        super(ResourcePage, self).__init__(*args, **kwargs)
        if self.get_parent():
            self.parent = self.get_parent().slug

    def get_context(self, request):
        context = super(ResourcePage, self).get_context(request)

        if 'ldmw_session' in request.COOKIES:
            cookie = request.COOKIES['ldmw_session']
            try:
                context['liked_value'] = Likes.objects\
                    .get(resource_id=self.id, user_hash=cookie)\
                    .like_value
            except:
                context['liked_value'] = 0
        else:
            cookie = ''
            context['liked_value'] = 0

        Home = apps.get_model('resources', 'home')
        landing_pages = Home.objects.filter(~Q(slug="home")).live()
        banner = Home.objects.get(slug="home").banner
        context['landing_pages'] = landing_pages
        context['banner'] = banner
        context['tags'] = combine_tags(self).specific.tags
        context['number_of_likes'] = Likes.objects\
            .filter(resource_id=self.id, like_value=1)\
            .count()
        context['number_of_dislikes'] = Likes.objects\
            .filter(resource_id=self.id, like_value=-1)\
            .count()

        return context

    class Meta:
        verbose_name = "Resource"
