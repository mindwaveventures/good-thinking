import json
import uuid

from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.db.models.fields import TextField, URLField
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from urllib.parse import parse_qs

from resources.models.tags import ExcludeTag
from resources.models.resources import ResourceIndexPage
from resources.models.helpers import (
    generate_custom_form, valid_request, handle_request, get_resource
)

from resources.views import get_data
from wagtail.wagtailcore.models import Orderable

uid = uuid.uuid4()


class FooterLink(models.Model):
    footer_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    footer_link = models.URLField(blank=True, )

    panels = [
        ImageChooserPanel('footer_image'),
        FieldPanel('footer_link'),
    ]

    class Meta:
        abstract = True


class HomeFooterLinks(Orderable, FooterLink):
    page = ParentalKey('Home', related_name='footer_links')


class FormField(AbstractFormField):
    page = ParentalKey('Home', related_name='form_fields')


class Home(AbstractForm):
    banner = RichTextField(
        blank=True,
        help_text="Banner at the top of every page"
    )
    header = RichTextField(
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

    def get_context(self, request):
        context = super(Home, self).get_context(request)

        return get_data(request, data=context, slug=self.slug)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('banner', classname="full"),
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
        FieldPanel('assessment_text', classname="full"),
        FieldPanel('crisis_text', classname="full"),
        FieldPanel('lookingfor', classname="full"),
        FieldPanel('alpha', classname="full"),
        FieldPanel('alphatext', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        InlinePanel('footer_links', label="Footer"),
    ]

    def process_form_submission(self, request_dict):
        if 'email' in request_dict or 'suggestion' in request_dict:
            page = Home.objects.get(slug='home')
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

    def serve(self, request, *args, **kwargs):
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

        form_fields = FormField.objects.all().filter(page_id=form.page.id)
        footer_links = HomeFooterLinks.all()

        context = self.get_context(request)
        context['form'] = form
        context['footer_links'] = footer_links

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
            context
        )
