from __future__ import unicode_literals

from django.db.models.fields import CharField
from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from resources.models.helpers import base_context


class StaticPage(Page):
    def get_context(self, request):
        context = super(StaticPage, self).get_context(request)

        return base_context(context,self)

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('heading', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock(template="static/display.html")),
        ('column_left', blocks.RichTextBlock(template="static/display.html")),
        ('column_right', blocks.RichTextBlock(template="static/display.html")),
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
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
    ]
