from wagtail.wagtailforms.models import AbstractForm, Page, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
)
from wagtail.wagtailsearch import index

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from django.db.models.fields import (
    TextField, URLField, IntegerField, CharField
)
from django.apps import apps
from django.db.models import Q
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from colorful.fields import RGBColorField

from resources.models.tags import (
    TopicTag, IssueTag, ReasonTag,
    ContentTag, HiddenTag
)

from likes.models import Likes

from resources.models.helpers import create_tag_combiner
from gpxpy.geo import haversine_distance


def check_latlong(self, latlong_input, n):
    """
        latlong_input :: string :: either the latitude or longitude input
        n :: positive integer ::
        representing the bounds for the inputs max and min
    """
    if latlong_input.strip() == "":
        return latlong_input
    try:
        if abs(float(latlong_input)) <= n:
            return latlong_input
        else:
            raise ValidationError(
                self.error_messages['invalid'], code='invalid'
            )
    except ValueError:
        raise ValidationError(
            self.error_messages['invalid'], code='invalid'
        )


class LatitudeField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid latitude.'),
    }

    # def __init__(self, **kwargs):
    #     super().__init__(strip=True, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        value = check_latlong(self, value, 90)
        return value


class LongitudeField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid longitude.'),
    }

    def to_python(self, value):
        value = super().to_python(value)
        value = check_latlong(self, value, 180)
        return value


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
    resource_url_text = TextField(
        blank=True,
        help_text="The text for the url link"
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
    latitude = LatitudeField(
        blank=True,
        max_length=255,
        help_text="""
            latitude. This should be a number between -90 and 90
        """
    )
    longitude = LongitudeField(
        blank=True,
        max_length=255,
        help_text="""
            longitude. This should be a number between -180 and 180
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
        FieldRowPanel([
            FieldPanel('resource_url', classname="col6"),
            FieldPanel('resource_url_text', classname="col6"),
        ], classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('pros', classname="full"),
        FieldPanel('cons', classname="full"),
        FieldPanel('video_url', classname="full"),
        MultiFieldPanel([
          FieldRowPanel([
              FieldPanel('latitude', classname="col6"),
              FieldPanel('longitude', classname="col6"),
          ], classname="full"),
        ], heading="latlong")
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

        if 'ldmw_location_latlong' in request.COOKIES:
            try:
                location = request.COOKIES['ldmw_location_latlong']
                [latitude, longitude] = location.split(",")
                dist_km = haversine_distance(
                    float(latitude), float(longitude),
                    float(self.latitude), float(self.longitude)
                )
                context['is_near'] = dist_km / 1.6 < 2000  # less than 2 miles
            except:
                print("Failed to get location")
                context['is_near'] = False
        else:
            context['is_near'] = False

        Home = apps.get_model('resources', 'home')
        Main = apps.get_model('resources', 'main')

        combine_tags = create_tag_combiner(None)

        landing_pages = Home.objects.filter(~Q(slug="home")).live()
        banner = Main.objects.get(slug="home").banner
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
