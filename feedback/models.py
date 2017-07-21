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

class FormBuilder(object):
    def __init__(self, fields):
        self.fields = fields

    def create_singleline_field(self, field, options):
        # TODO: This is a default value - it may need to be changed
        options['max_length'] = 255
        return django.forms.CharField(**options)

    def create_multiline_field(self, field, options):
        return django.forms.CharField(widget=django.forms.Textarea, **options)

    def create_date_field(self, field, options):
        return django.forms.DateField(**options)

    def create_datetime_field(self, field, options):
        return django.forms.DateTimeField(**options)

    def create_email_field(self, field, options):
        return django.forms.EmailField(**options)

    def create_url_field(self, field, options):
        return django.forms.URLField(**options)

    def create_number_field(self, field, options):
        return django.forms.DecimalField(**options)

    def create_dropdown_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.ChoiceField(**options)

    def create_multiselect_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.MultipleChoiceField(**options)

    def create_radio_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)

    def create_checkboxes_field(self, field, options):
        options['choices'] = [(x.strip(), x.strip()) for x in field.choices.split(',')]
        options['initial'] = [x.strip() for x in field.default_value.split(',')]
        return django.forms.MultipleChoiceField(
            widget=django.forms.CheckboxSelectMultiple, **options
        )

    def create_checkbox_field(self, field, options):
        return django.forms.BooleanField(**options)

    FIELD_TYPES = {
        'singleline': create_singleline_field,
        'multiline': create_multiline_field,
        'date': create_date_field,
        'datetime': create_datetime_field,
        'email': create_email_field,
        'url': create_url_field,
        'number': create_number_field,
        'dropdown': create_dropdown_field,
        'multiselect': create_multiselect_field,
        'radio': create_radio_field,
        'checkboxes': create_checkboxes_field,
        'checkbox': create_checkbox_field,
    }

    @property
    def formfields(self):
        formfields = OrderedDict()

        for field in self.fields:
            options = self.get_field_options(field)

            if field.field_type in self.FIELD_TYPES:
                formfields[field.clean_name] = self.FIELD_TYPES[field.field_type](self, field, options)
            else:
                raise Exception("Unrecognised field type: " + field.field_type)

        return formfields

    def get_field_options(self, field):
        options = {}
        options['label'] = field.label
        options['help_text'] = field.help_text
        options['required'] = field.required
        options['initial'] = field.default_value
        # options['before_input'] = field.before_input
        # options['after_input'] = field.after_input
        return options

    def get_form_class(self):
        return type(str('WagtailForm'), (BaseForm,), self.formfields)

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
    form_builder = FormBuilder

    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")

    content_panels = AbstractForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('alphatext', classname="full"),
    ]

    def get_form_fields(self):
        """
        Form page expects `form_fields` to be declared.
        If you want to change backwards relation name,
        you need to override this method.
        """

        return self.form_fields.all()

    def get_data_fields(self):
        """
        Returns a list of tuples with (field_name, field_label).
        """

        data_fields = [
            ('submit_time', _('Submission date')),
        ]
        data_fields += [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        return data_fields

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields())
        return fb.get_form_class()

    def get_form_parameters(self):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        return form_class(*args, **form_params)

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

        custom_form = []

        vals = FormField.objects.all().filter(page_id=form.page.id)

        for val in vals:
            dict = {}
            dict['before_input'] = val.before_input
            dict['after_input'] = val.after_input
            dict['field_type'] = val.field_type
            dict['default_value'] = val.default_value
            dict['label'] = val.label

            if form.errors:
                try:
                    dict['errors'] = form.errors.as_data()[val.label][0]
                except:
                    pass

            if val.field_type == 'radio':
                dict['choices'] = val.choices.split(",")

            if val.required:
                dict['required'] = 'required'
            else:
                dict['required'] = ''

            custom_form.append(dict)

        context = self.get_context(request)
        context['form'] = form
        context['custom_form'] = custom_form

        return render(
            request,
            self.get_template(request),
            context
       ) 
