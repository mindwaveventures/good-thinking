import json
import django

from collections import OrderedDict

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models
from django.db.models.fields import TextField
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from django.utils.translation import ugettext_lazy as _

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField, AbstractFormSubmission

from wagtail.wagtailforms.forms import BaseForm

FORM_FIELD_CHOICES = (
    ('singleline', _('Single line text')),
    ('multiline', _('Multi-line text')),
    ('email', _('Email')),
    ('number', _('Number')),
    ('url', _('URL')),
    ('checkbox', _('Checkbox')),
    ('checkboxes', _('Checkboxes')),
    ('dropdown', _('Drop down')),
    ('multiselect', _('Multiple select')),
    ('radio', _('Radio buttons')),
    ('date', _('Date')),
    ('datetime', _('Date/time')),
)

class FormField(AbstractFormField):
    page = ParentalKey('FeedbackPage', related_name='form_fields')
    label = models.CharField(
        verbose_name=_('label'),
        max_length=255,
        help_text=_('The label of the form field')
    )
    field_type = models.CharField(verbose_name=_('field type'), max_length=16, choices=FORM_FIELD_CHOICES)
    required = models.BooleanField(verbose_name=_('required'), default=True)
    choices = models.TextField(
        verbose_name=_('choices'),
        blank=True,
        help_text=_('Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')
    )
    default_value = models.CharField(
        verbose_name=_('default value'),
        max_length=255,
        blank=True,
        help_text=_('Default value. Comma separated values supported for checkboxes.')
    )
    before_input = RichTextField(verbose_name=_('before input'), blank=True)
    after_input = RichTextField(verbose_name=_('after input'), blank=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('before_input'),
        FieldPanel('after_input'),
        FieldPanel('required'),
        FieldPanel('field_type', classname="formbuilder-type"),
        FieldPanel('choices', classname="formbuilder-choices"),
        FieldPanel('default_value', classname="formbuilder-default"),
    ]

class FeedbackPage(AbstractForm):
    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")

    content_panels = AbstractForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('alphatext', classname="full"),
    ]

    # to see how the serve function has been edited, see the original function here:
    # https://github.com/wagtail/wagtail/blob/master/wagtail/wagtailforms/models.py#L238
    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)

                # render the landing_page
                # TODO: It is much better to redirect to it
                return render(
                    request,
                    self.get_landing_page_template(request),
                    self.get_context(request)
                )
        else:
            form = self.get_form(page=self, user=request.user)

        # custom
        custom_form = []

        vals = FormField.objects.all().filter(page_id=form.page.id)

        for val in vals:
            dict = {}
            dict['before_input'] = val.before_input
            dict['after_input'] = val.after_input
            dict['field_type'] = val.field_type
            dict['default_value'] = val.default_value
            dict['label'] = val.label

            # pull through errors when form is invalid
            # TODO: look at a nicer way to fetch out the errors
            if form.errors:
                try:
                    dict['errors'] = form.errors.as_data()[val.label][0]
                except:
                    pass

            dict['choices'] = val.choices.split(",") # dict['choices'] only being used in template if val.field_type is 'radio'

            dict['required'] = 'required' if val.required else ''

            custom_form.append(dict)

        context = self.get_context(request)
        context['form'] = form
        context['custom_form'] = custom_form # custom

        return render(
            request,
            self.get_template(request),
            context
       ) 
