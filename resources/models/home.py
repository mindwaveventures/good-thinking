import json
import uuid
import re

from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.db.models.fields import TextField, URLField, CharField
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import Http404
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from urllib.parse import parse_qs

from resources.models.tags import ExcludeTag
from resources.models.resources import ResourceIndexPage
from resources.models.helpers import (
    generate_custom_form, valid_request,
    handle_request, get_resource, base_context
)

from resources.views import get_data
from wagtail.wagtailcore.models import Orderable

uid = uuid.uuid4()


def check_two_letter_zipcode(self, value):
    if value.strip() == "" or re.match(r"^[A-Za-z][A-Za-z]?$", value):
        return value
    else:
        raise ValidationError(
            self.error_messages['invalid'], code='invalid'
        )


class TwoCharsZipcodeField(CharField):
    default_error_messages = {
        'invalid': _('Enter one or 2 letters of the zipcode'),
    }

    def to_python(self, value):
        value = super().to_python(value)
        value = check_two_letter_zipcode(self, value)
        return value


class LocationImages(models.Model):
    location_image = models.ForeignKey(
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
    first_letters_of_zip = TwoCharsZipcodeField(
        blank=True,
        max_length=255,
        help_text="""
            The first letter or letters of the postcode
            you would like to match with, e.g. TW or E
        """
    )

    panels = [
        FieldPanel('location_image', classname="col6"),
        FieldPanel('first_letters_of_zip', classname="col6"),
    ]

    class Meta:
        abstract = True


class MainLocationImages(Orderable, LocationImages):
    page = ParentalKey('Main', related_name='location_images')


class FooterLink(models.Model):
    footer_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    footer_link = models.URLField(blank=True,)

    panels = [
        ImageChooserPanel('footer_image'),
        FieldPanel('footer_link'),
    ]

    class Meta:
        abstract = True


class FooterBlock(models.Model):
    title = TextField(blank=True,)
    description = RichTextField(blank=True,)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link_text = TextField(blank=True,)

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('title', classname="title"),
        FieldPanel('description', classname="full"),
        FieldPanel('link_text'),
    ]

    class Meta:
        abstract = True


class HomeFooterLinks(Orderable, FooterLink):
    page = ParentalKey('Main', related_name='footer_links')


class HomeFooterBlocks(Orderable, FooterBlock):
    page = ParentalKey('Main', related_name='footer_blocks')


class ProjectInfoBlock(Orderable, FooterBlock):
    page = ParentalKey('Main', related_name='project_info_block')


class FormField(AbstractFormField):
    page = ParentalKey('Home', related_name='form_fields')


class MainFormField(AbstractFormField):
    page = ParentalKey('Main', related_name='form_fields')


class Home(AbstractForm):
    def route(self, request, path_components):
        if path_components:
            return RouteResult(
                self, kwargs={'path_components': path_components}
            )
        else:
            if self.live:
                return RouteResult(self)
            else:
                raise Http404

    banner = RichTextField(
        blank=True,
        help_text="Banner at the top of every page"
    )
    header = TextField(
        blank=True,
        help_text="Hero title"
    )
    body = RichTextField(
        blank=True,
        help_text="Description of page"
    )
    filter_label_1 = TextField(
        blank=True,
        help_text="Label/Question for first set of filters"
    )
    filter_label_2 = TextField(
        blank=True,
        help_text="Label/Question for second set of filters"
    )
    filter_label_3 = TextField(
        blank=True,
        help_text="Label/Question for third set of filters"
    )
    assessment_text = RichTextField(
        blank=True,
        help_text="Label for sleep assessment link"
    )
    crisis_text = RichTextField(
        blank=True,
        help_text="Label for sleep crisis page link"
    )
    lookingfor = RichTextField(
        blank=True,
        help_text="""
        Information on how to leave suggestions and what they are for
        """
    )
    alpha = RichTextField(
        blank=True,
        help_text="What is Alpha"
    )
    alphatext = RichTextField(
        blank=True,
        help_text="Why to take part in the alpha"
    )
    footer = RichTextField(blank=True, help_text="Footer text")
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
    video_url = URLField(
        blank=True,
        help_text="URL of an introductiary youtube video"
    )
    exclude_tags = ClusterTaggableManager(
        through=ExcludeTag, blank=True, verbose_name="Exclude Tags",
        help_text="""
        Tags you do not want to show in the filters for this home page
        """
    )
    description = RichTextField(blank=True, help_text="""
        A short description of the page that will show on the homepage
    """)
    link_text = TextField(
        blank=True,
        help_text="Text to display for the link to this page"
    )
    mobile_title = TextField(
        blank=True,
        help_text="Title to show on mobile"
    )

    def get_context(self, request, **kwargs):
        context = super(Home, self).get_context(request)

        context = get_data(
            request, data=context, slug=self.slug,
            path_components=kwargs.get('path_components', [])
        )

        return context

    content_panels = AbstractForm.content_panels + [
        MultiFieldPanel([
            FieldPanel('description'),
            FieldPanel('link_text'),
            FieldPanel('mobile_title')
        ], heading="Link Block"),
        ImageChooserPanel('hero_image'),
        FieldPanel('header', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('video_url', classname="full"),
        MultiFieldPanel([
            FieldPanel('filter_label_1', classname="full"),
            FieldPanel('filter_label_2', classname="full"),
            FieldPanel('filter_label_3', classname="full"),
            FieldPanel('exclude_tags', classname="full")
        ]),
    ]

    def process_form_submission(self, request_dict):
        return custom_form_submission(self, request_dict)

    def serve(self, request, *args, **kwargs):
        path_components = kwargs.get('path_components', [])
        return custom_serve(**locals())


class Main(AbstractForm):
    banner = RichTextField(
        blank=True,
        help_text="Banner at the top of every page"
    )
    header = TextField(
        blank=True,
        help_text="Hero title"
    )
    body = RichTextField(
        blank=True,
        help_text="Description of page"
    )
    filter_label_1 = TextField(
        blank=True,
        help_text="Label/Question for first set of filters"
    )
    filter_label_2 = TextField(
        blank=True,
        help_text="Label/Question for second set of filters"
    )
    filter_label_3 = TextField(
        blank=True,
        help_text="Label/Question for third set of filters"
    )
    lookingfor = RichTextField(
        blank=True,
        help_text="""
        Information on how to leave suggestions and what they are for
        """
    )
    alpha = RichTextField(
        blank=True,
        help_text="What is Alpha"
    )
    alphatext = RichTextField(
        blank=True,
        help_text="Why to take part in the alpha"
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

    content_panels = AbstractForm.content_panels + [
        FieldPanel('banner', classname="full"),
        ImageChooserPanel('hero_image'),
        InlinePanel('location_images', label="Location Images"),
        FieldPanel('header', classname="full"),
        FieldPanel('body', classname="full"),
        InlinePanel('project_info_block', label="Project Info Block"),
        MultiFieldPanel([
            FieldPanel('filter_label_1', classname="full"),
            FieldPanel('filter_label_2', classname="full"),
            FieldPanel('filter_label_3', classname="full")
        ]),
        FieldPanel('lookingfor', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        InlinePanel('footer_blocks', label="Footer Blocks"),
        InlinePanel('footer_links', label="Footer"),
    ]

    def get_context(self, request, **kwargs):
        context = super(Main, self).get_context(request)
        if 'ldmw_location_zipcode' in request.COOKIES:
            try:
                zipcode = request.COOKIES['ldmw_location_zipcode']
                for loc_img in MainLocationImages.objects.all():
                    short_zip = loc_img.first_letters_of_zip
                    if zipcode[:len(short_zip)] == short_zip:
                        location_hero_image = loc_img.location_image
                        break
                if not location_hero_image:
                    location_hero_image = self.hero_image
                context['hero_image'] = location_hero_image
            except:
                context['hero_image'] = self.hero_image
        else:
            context['hero_image'] = self.hero_image
        return get_data(request, data=context, slug=self.slug)

    def process_form_submission(self, request_dict):
        return custom_form_submission(self, request_dict)

    def serve(self, request, *args, **kwargs):
        return custom_serve(**locals())


def custom_serve(self, request, *args, **kwargs):
    try:
        request_dict = parse_qs(request.body.decode('utf-8'))
    except:
        request_dict = request.POST.dict()

        id = request_dict['id']

        self.process_form_submission(request_dict)

        try:
            cookie = request.COOKIES['ldmw_session']
        except:
            cookie = uid.hex

        resource = get_resource(id, cookie)

        resource_result = render_to_string(
            'resources/resource.html',
            {'page': resource, 'like_feedback_submitted': True}
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

    if request.method == 'POST':
        form = self.get_form(request.POST, page=self, user=request.user)
        if form.is_valid():
            self.process_form_submission(request_dict)

            if valid_request(request_dict):
                return handle_request(
                  request,
                  request_dict,
                  HttpResponseRedirect,
                  messages
                )

    else:
        form = self.get_form(page=self, user=request.user)

    if str(self.__class__.__name__) == 'Main':
        form_fields = MainFormField.objects.all().filter(page_id=form.page.id)
    elif str(self.__class__.__name__) == 'Home':
        form_fields = FormField.objects.all().filter(page_id=form.page.id)
    else:
        form_fields = None

    project_info_block = ProjectInfoBlock.objects.all()

    path_components = kwargs.get('path_components', [])

    list(map(lambda x: " ".join(x.split("-")), path_components))

    context = self.get_context(request, path_components=path_components)
    context['form'] = form
    context['project_info_block'] = project_info_block

    like_feedback_submitted = False
    for m in messages.get_messages(request):
        if m.__str__()[:14] == 'like_feedback_':
            like_feedback_submitted = True

    context['like_feedback_submitted'] = like_feedback_submitted
    context['custom_form'] = generate_custom_form(
        form_fields,
        request_dict,
        messages.get_messages(request)
    )  # custom

    return render(
        request,
        self.get_template(request),
        base_context(context)
    )


def custom_form_submission(self, request_dict):
    if 'email' in request_dict or 'suggestion' in request_dict:
        page = Main.objects.get(slug='home')
        try:
            email = request_dict['email'][0]
        except:
            email = ''
        try:
            suggestion = request_dict['suggestion'][0]
        except:
            suggestion = ''

        form_data = {'email': email, 'suggestion': suggestion}
    else:
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
