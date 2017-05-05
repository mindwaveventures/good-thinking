from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import TextField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)
    lookingfor = RichTextField(blank=True)
    alphatext = RichTextField(blank=True)
    footer = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('lookingfor', classname="full"),
        FieldPanel('alphatext', classname="full"),
        FieldPanel('footer', classname="full"),
    ]
