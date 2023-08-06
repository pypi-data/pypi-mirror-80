from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class IndexPage(Page):
    intro = RichTextField(blank=True)

class AyewaIndexPage(IndexPage):

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class SolutionIndexPage(IndexPage):

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class Solution(Page):
    description = RichTextField('Description', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'