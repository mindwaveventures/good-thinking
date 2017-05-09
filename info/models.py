from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class InfoPage(Page):
    body = RichTextField(blank=True)
    heading = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('body', classname="full"),
    ]
