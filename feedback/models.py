from modelcluster.fields import ParentalKey

from django.db import models
from django.db.models.fields import TextField

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField

class FormField(AbstractFormField):
    page = ParentalKey('FeedbackPage', related_name='form_fields')

class FeedbackPage(AbstractForm):
    form_title = TextField(blank=True)

    feedback1_intro = RichTextField(blank=True)
    feedback1_default_text = TextField(blank=True)
    feedback1_help_text = RichTextField(blank=True)

    feedback2_intro = RichTextField(blank=True)
    feedback2_default_text = TextField(blank=True)
    feedback2_help_text = RichTextField(blank=True)

    alpha = RichTextField(blank=True, help_text="What is Alpha")
    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")

    content_panels = AbstractForm.content_panels + [
        FieldPanel('form_title', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldPanel('feedback1_intro', classname="full"),
            FieldRowPanel([
                FieldPanel('feedback1_default_text', classname="col6"),
                FieldPanel('feedback1_help_text', classname="col6")
            ])
        ], "Feedback1"),
        MultiFieldPanel([
            FieldPanel('feedback2_intro', classname="full"),
            FieldRowPanel([
                FieldPanel('feedback2_default_text', classname="col6"),
                FieldPanel('feedback2_help_text', classname="col6")
            ])
        ], "Feedback2"),
        FieldPanel('alpha', classname="full"),
        FieldPanel('alphatext', classname="full"),
    ]
