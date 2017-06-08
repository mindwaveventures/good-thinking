from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import TextField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class HomePage(Page):
    banner = RichTextField(blank=True, help_text="Banner at the top of every page")
    body = RichTextField(blank=True, help_text="Description of page")
    filter_label_1 = TextField(blank=True, help_text="Label/Question for first set of filters")
    filter_label_2 = TextField(blank=True, help_text="Label/Question for second set of filters")
    filter_label_3 = TextField(blank=True, help_text="Label/Question for third set of filters")
    assessment_text = RichTextField(blank=True, help_text="Label for sleep assessment link")
    crisis_text = RichTextField(blank=True, help_text="Label for sleep crisis page link")
    lookingfor = RichTextField(blank=True, help_text="Information on how to leave suggestions and what the suggestions are for")
    alpha = RichTextField(blank=True, help_text="What is Alpha")
    alphatext = RichTextField(blank=True, help_text="Why to take part in the alpha")
    footer = RichTextField(blank=True, help_text="Footer text")

    content_panels = Page.content_panels + [
        FieldPanel('banner', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('filter_label_1', classname="full"),
        FieldPanel('filter_label_2', classname="full"),
        FieldPanel('filter_label_3', classname="full"),
        FieldPanel('assessment_text', classname="full"),
        FieldPanel('crisis_text', classname="full"),
        FieldPanel('lookingfor', classname="full"),
        FieldPanel('alpha', classname="full"),
        FieldPanel('alphatext', classname="full"),
        FieldPanel('footer', classname="full"),
    ]
