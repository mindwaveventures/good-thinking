import uuid
import json

from wagtail.wagtailforms.models import AbstractForm, Page, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel,PageChooserPanel
)
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
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
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from resources.views import get_data, filter_resources
from colorful.fields import RGBColorField
from urllib.parse import parse_qs
from resources.models.tags import (
    TopicTag, IssueTag, ReasonTag,
    ContentTag, HiddenTag
)
from likes.models import Likes

from resources.models.helpers import (
    create_tag_combiner, base_context, get_resource
)
from resources.views import assessment_controller
from gpxpy.geo import haversine_distance

uid = uuid.uuid4()


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

    def to_python(self, value):
        value = super().to_python(value)
        value = check_latlong(self, value, 90)
        return value

    class Meta:
        abstract = True


class LongitudeField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid longitude.'),
    }

    def to_python(self, value):
        value = super().to_python(value)
        value = check_latlong(self, value, 180)
        return value

    class Meta:
        abstract = True


class Badges(models.Model):
    badge_color = RGBColorField(
        default='#ffffff', null=True, blank=True
    )
    badge_text_color = RGBColorField(
        default='#000000', null=True, blank=True
    )
    badge_text = TextField(blank=True)

    panels = [
        FieldPanel('badge_color'),
        FieldPanel('badge_text_color'),
        FieldPanel('badge_text')
    ]

    class Meta:
        abstract = True


class ResourcePageBadges(Orderable, Badges):
    page = ParentalKey('ResourcePage', related_name='badges')


class Buttons(models.Model):
    BUTTON_TYPES = (
      ('Primary', 'Primary'),
      ('Secondary', 'Secondary')
    )
    button_type = CharField(
      choices=BUTTON_TYPES,
      default='Primary',
      max_length=16,
      help_text='Type of Button - Primary/Secondary'
    )
    button_text = TextField()
    button_link = URLField()

    ALIGNMENT_CHOICES = (
      ('tl', 'left'),
      ('tc', 'center'),
      ('tr', 'right')
    )
    alignment = CharField(
      choices=ALIGNMENT_CHOICES,
      max_length=10,
      default='left',
      help_text='Alignment of the button'
    )

    panels = [
        FieldPanel('button_type'),
        FieldPanel('button_text'),
        FieldPanel('button_link'),
        FieldPanel('alignment')
    ]

    class Meta:
        abstract = True


class ResourcePageButtons(Orderable, Buttons):
    page = ParentalKey('ResourcePage', related_name='buttons')


class LatLong(Orderable):
    latitude = LatitudeField(max_length=10)
    longitude = LongitudeField(max_length=10)

    panels = [
        FieldPanel('latitude'),
        FieldPanel('longitude')
    ]

    page = ParentalKey('ResourcePage', related_name='latlong')


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


def custom_form_submission(self, request_dict):
    page = ResourceIndexPage.objects.get(slug="resources")
    form_data = {
        'resource_title': request_dict['resource_title'],
        'resource_name': request_dict['resource_name'],
        'feedback': request_dict['feedback'],
        'liked': request_dict['liked'],
    }

    return self.get_submission_class().objects.create(
        form_data=json.dumps(form_data, cls=DjangoJSONEncoder),
        page=page,
    )


class ResourcePage(AbstractForm):
    def process_form_submission(self, request_dict):
        return custom_form_submission(self, request_dict)

    def serve(self, request, *args, **kwargs):
        try:
            request_dict = request.POST.dict()

            id = request_dict['id']

            self.process_form_submission(request_dict)

            try:
                cookie = request.COOKIES['ldmw_session']
            except:
                cookie = uid.hex

            resource = get_resource(id, cookie)

            if request_dict['feedback'] == '':
                error = True
            else:
                error = False

            csrf = request.POST.get('csrfmiddlewaretoken')

            resource_result = render_to_string(
                'resources/resource.html',
                {
                    'page': resource, 'like_feedback_submitted': True,
                    'error': error, 'csrf_token': csrf
                }
            )

            visited_result = render_to_string(
                'resources/single_visited.html',
                {'v': resource, 'like_feedback_submitted': True}
            )

            return JsonResponse({
                'result': resource_result,
                'visited_result': visited_result,
                'id': id,
                'feedback': True
            })

        except:
            request.is_preview = getattr(request, 'is_preview', False)

            return TemplateResponse(
                request,
                self.get_template(request, *args, **kwargs),
                self.get_context(request, *args, **kwargs)
            )

    form_fields = None

    heading = TextField(
        blank=True,
        help_text="The title of the resource being linked to"
    )
    logo_background_color = RGBColorField(
        default='#16b28f', null=True, blank=True,
        help_text="The background colour of brand_logo"
    )
    resource_url = URLField(
        blank=True,
        help_text="The url of the resource to link to"
    )
    resource_url_text = TextField(
        blank=True,
        help_text="The text for the url link"
    )
    tagline = RichTextField(
        blank=True,
        help_text="Bold text that displays on the resource list"
    )
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('heading', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('column_left', blocks.RichTextBlock()),
        ('column_right', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    pros = RichTextField(
        blank=True,
        help_text="A list of pros for the resource"
    )
    cons = RichTextField(
        blank=True,
        help_text="A list of cons for the resource"
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
        InlinePanel('badges', label="Badge"),
        InlinePanel('latlong', label="Latitude and Longitude"),
        FieldPanel('heading', classname="full"),
        FieldPanel('logo_background_color', classname="full"),
        FieldRowPanel([
            FieldPanel('resource_url', classname="col6"),
            FieldPanel('resource_url_text', classname="col6"),
        ], classname="full"),
        FieldPanel('tagline', classname="full"),
        StreamFieldPanel('body'),
        InlinePanel('buttons', label="Buttons"),
        FieldPanel('pros', classname="full"),
        FieldPanel('cons', classname="full")
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
        self.__class__.objects.prefetch_related('tagged_items__tag')
        super(ResourcePage, self).__init__(*args, **kwargs)
        try:
            self.parent = self.get_parent().slug
        except:
            self.parent = None

    def get_context(self, request):
        context = super(ResourcePage, self).get_context(request)

        if (
            request.META.get('HTTP_REFERER') and
            request.session.get('results_page')
        ):
            context['back'] = request.session.pop('results_page')

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
                [user_lat, user_long] = location.split(",")
                context['is_near'] = any(
                    filter(
                        lambda e: haversine_distance(
                            float(user_lat), float(user_long),
                            float(e.latitude), float(e.longitude)
                        ) / 1.6 < 1000, self.latlong.all())
                    )
                # less than 1 mile
            except:
                print("Failed to get location")
                context['is_near'] = False
        else:
            context['is_near'] = False

        Home = apps.get_model('resources', 'home')

        combine_tags = create_tag_combiner(None)
        landing_pages = Home.objects.filter(~Q(slug="home")).live()

        context['landing_pages'] = landing_pages
        context['tags'] = combine_tags(self).specific.tags
        context['number_of_likes'] = Likes.objects\
            .filter(resource_id=self.id, like_value=1)\
            .count()
        context['number_of_dislikes'] = Likes.objects\
            .filter(resource_id=self.id, like_value=-1)\
            .count()
        context['badges'] = ResourcePageBadges.objects\
            .filter(page_id=self.page_ptr_id)
        context['buttons'] = ResourcePageButtons.objects\
            .filter(page_id=self.page_ptr_id)

        return base_context(context,self)

    def get_form_fields(self):
        return iter([])

    def likes(self):
        return Likes.objects\
            .filter(resource_id=self.id, like_value=1)\
            .count()

    def dislikes(self):
        return Likes.objects\
            .filter(resource_id=self.id, like_value=-1)\
            .count()

    class Meta:
        verbose_name = "Resource"


class Tip(ResourcePage):
    tip_text = RichTextField(blank=True)
    credit = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('tip_text', classname="full"),
        FieldPanel('credit', classname="full")
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('topic_tags'),
        FieldPanel('issue_tags'),
        FieldPanel('reason_tags'),
        FieldPanel('content_tags'),
        FieldPanel('hidden_tags'),
        FieldPanel('priority'),
    ]

class Results(ResourcePage):
    cover_image = models.ForeignKey(
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
    image_text = TextField(blank=True)
    body_title = TextField(blank=True)
    body_tagline = TextField(blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover_image'),
        FieldPanel('image_text', classname="full"),
        FieldPanel('body_title', classname="full"),
        FieldPanel('body_tagline', classname="full")
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('topic_tags'),
        FieldPanel('issue_tags'),
        FieldPanel('reason_tags'),
        FieldPanel('content_tags'),
        FieldPanel('hidden_tags'),
        FieldPanel('priority'),
    ]

    def get_context(self, request, **kwargs):
        try:
            query = request.GET.urlencode()
            slug = parse_qs(query)['slug'][0]
        except:
            slug = ''
        context = super(Results, self).get_context(request)
        context = get_data(
            request, data=context, slug=slug,
            path_components=kwargs.get('path_components', [])
        )
        return base_context(context,self)

class SelectResources(models.Model):
    collection_resource = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('collection_resource'),
    ]

    class Meta:
        abstract = True

class ResourcePageSelectResources(Orderable, SelectResources):
    page = ParentalKey('TopResources', related_name='selectresources')

class TopResources(ResourcePage):
    collection_heading = TextField(blank=True)
    description = TextField(blank=True)
    button_text = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('collection_heading', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('button_text', classname="full"),
        InlinePanel('selectresources', label="selectresources"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('topic_tags'),
        FieldPanel('priority'),
    ]

    def get_context(self, request, **kwargs):
        try:
            query = request.GET.urlencode()
            slug = parse_qs(query)['slug'][0]
        except:
            slug = ''
        context = super(Results, self).get_context(request)
        context = get_data(
            request, data=context, slug=slug,
            path_components=kwargs.get('path_components', [])
        )
        return base_context(context,self)

class Assessment(ResourcePage):
    algorithm_id = IntegerField(
        default=4648,
        help_text='The ID of the assessment algorithm'
    )

    resource_text = RichTextField(
        blank=True,
        help_text=(
            "An intro to the resources attached to the assessment results"
        )
    )

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        StreamFieldPanel('body'),
        FieldPanel('algorithm_id', classname="full"),
        FieldPanel('resource_text', classname="full")
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('topic_tags'),
        FieldPanel('issue_tags'),
        FieldPanel('reason_tags'),
        FieldPanel('content_tags'),
        FieldPanel('hidden_tags'),
        FieldPanel('priority'),
    ]

    def get_context(self, request):
        context = super(Assessment, self).get_context(request)

        return base_context(context,self)

    def serve(self, request, *args, **kwargs):
        return assessment_controller(self, request, **kwargs)


class ResourceAdmin(ModelAdmin):
    model = ResourcePage
    list_display = ('title', 'likes', 'dislikes',)


modeladmin_register(ResourceAdmin)
