from modelcluster.fields import ParentalKey

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.fields import TextField

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from wagtail.wagtailadmin.edit_handlers import FieldPanel

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

class CmsFormField(AbstractFormField):
    def __init__(cls, name, bases, attrs):
        cls.page = ParentalKey(cls.parental_key, related_name='form_fields')
        super(CmsFormField, cls).__init__(name, bases, attrs)

        # if cls.custom_panels:
        #     label = models.CharField(
        #         verbose_name=_('label'),
        #         max_length=255,
        #         help_text=_('The label of the form field')
        #     )
        #     field_type = models.CharField(
        #         verbose_name=_('field type'),
        #         max_length=16,
        #         choices=FORM_FIELD_CHOICES
        #     )
        #     required = models.BooleanField(
        #         verbose_name=_('required'),
        #         default=True
        #     )
        #     choices = models.TextField(
        #         verbose_name=_('choices'),
        #         blank=True,
        #         help_text=_('Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')
        #     )
        #     default_value = models.CharField(
        #         verbose_name=_('default value'),
        #         max_length=255,
        #         blank=True,
        #         help_text=_('Default value. Comma separated values supported for checkboxes.')
        #     )
        #     before_input = RichTextField(
        #         verbose_name=_('before input'),
        #         blank=True
        #     ) # custom
        #     after_input = RichTextField(
        #         verbose_name=_('after input'),
        #         blank=True
        #     ) # custom

        #     cls.panels = [
        #         FieldPanel('label'),
        #         # FieldPanel('help_text'), # removed help_text as we instead use rich text
        #         FieldPanel('required'),
        #         FieldPanel('before_input'), # custom
        #         FieldPanel('after_input'), # custom
        #         FieldPanel('field_type', classname="formbuilder-type"),
        #         FieldPanel('choices', classname="formbuilder-choices"),
        #         FieldPanel('default_value', classname="formbuilder-default"),
        #     ]

