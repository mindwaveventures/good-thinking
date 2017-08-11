from __future__ import unicode_literals

from django.db import models

from django.db.models.fields import CharField

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock

from resources.models.home import Home


class StaticPage(Page):
    def get_context(self, request):
        context = super(StaticPage, self).get_context(request)

        home = Home.objects.first()

        context['banner'] = home.banner
        context['footer'] = home.footer
        return context

    body = StreamField([
        ('heading', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    ALIGNMENT_CHOICES = (
      ('tl', 'left'),
      ('tc', 'center')
    )
    text_alignment = CharField(
      choices=ALIGNMENT_CHOICES,
      max_length=10,
      default='left',
      help_text='Text Alignment'
    )

    content_panels = Page.content_panels + [
        FieldPanel('text_alignment'),
        StreamFieldPanel('body'),
    ]
