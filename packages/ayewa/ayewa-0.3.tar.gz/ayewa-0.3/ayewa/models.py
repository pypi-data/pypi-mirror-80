from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, FieldRowPanel


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
        FieldPanel('description', classname="full"),

    ]

    def __str__(self):
        try:
            return '{name}'.format(
                name=self.name,
            )
        except AttributeError:
            return 'unassigned'

class Resource(Page):
    summary = models.TextField(_('Summary'), default='', blank=True, null=True)
    description = RichTextField('Description', blank=True)
    # resource_type = models.ForeignKey(ResourceType, blank=True, null=True, related_name='resource_type')
    # user_rating = models.ForeignKey(UserRating, blank=True, null=True, related_name='rating')
    # internal_rating = models.ForeignKey(InternalRating, blank=True, null=True, related_name='internal_rating')
    # rank = models.ForeignKey(Rank, blank=True, null=True, related_name='rank')
    # resource_class = models.ManyToManyField(ResourceClass, blank=True, related_name='resource_class')
    # resource_need = models.ManyToManyField(ResourceNeed, blank=True, related_name='resource_need')
    # scope = models.ManyToManyField(Scope, blank=True, related_name='scope')
    # solutionon = models.ManyToManyField(Solution, blank=True, related_name='solution')
    email_address = models.CharField(_('Email Address'), max_length=64, blank=True, default='')
    primary_phone = models.CharField(_('Primary Phone'), max_length=50, blank=True, null=True, default=None)
    address_1 = models.CharField(_('Address 1'), max_length=64, blank=True, null=True, default='')
    address_2 = models.CharField(_('Address 2'), max_length=64, blank=True, null=True, default=None)
    city = models.CharField(_('City'), max_length=64, blank=True, null=True, default='')
    state = models.CharField(_('State'), max_length=20, blank=True, default='')
    postal_code = models.CharField(_('Postal (Zip) Code'), max_length=10, blank=True, null=True, default='',
                                   validators=[])  # TODO: Add a validator
    country = models.CharField(_('Country'), max_length=30, blank=True, null=True, default='',
                               validators=[])  # TODO: Add a validator
    website = models.CharField(_('Website'), max_length=30, blank=True, null=True, default='',
                               validators=[])  # TODO: Add a validator

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('summary', classname="full"),
        FieldRowPanel([
            FieldPanel('email_address',),
            FieldPanel('primary_phone',)
        ]),
        FieldPanel('address_1', classname="full"),
        FieldPanel('address_2', classname="full"),
        FieldRowPanel([
            FieldPanel('city', ),
            FieldPanel('state',),

        ]),
        FieldRowPanel([
            FieldPanel('postal_code', ),
            FieldPanel('country', ),

        ]),
        FieldPanel('website', classname="full"),
    ]

    def __str__(self):
        try:
            classes = ', '.join(self.list_resource_classes())
            if classes:
                classes = '({classes})'.format(classes=classes)
            return '{name} {classes}'.format(
                name=self.name,
                classes=classes
            )
        except AttributeError:
            return 'unassigned'

    def list_resource_classes(self):
        return ['{name}'.format(name=i.name) for i in self.resource_class.all()]

    def list_resource_classes_as_str(self):
        classes = ', '.join(self.list_resource_classes())
        return '{classes}'.format(
            classes=classes
        )

    def list_scopes(self):
        return ['{name}'.format(name=i.name) for i in self.scope.all()]

    def list_scopes_as_str(self):
        scopes = ', '.join(self.list_scopes())
        return '{scopes}'.format(
            scopes=scopes
        )

    def list_solutions(self):
        return ['{name}'.format(name=i.name) for i in self.solution.all()]

    def list_solutions_as_str(self):
        solutions = ', '.join(self.list_solutions())
        return '{solutions}'.format(
            solutions=solutions
        )

    def list_needs(self):
        return ['{name}'.format(name=i.name) for i in self.resource_need.all()]

    def list_needs_as_str(self):
        needs = ', '.join(self.list_needs())
        return '{needs}'.format(
            needs=needs
        )

    def is_project(self):
        if len(self.resource_class.filter(is_project=True)) > 0:
            return True
        else:
            return False

    def is_organization(self):
        if len(self.resource_class.filter(is_organization=True)) > 0:
            return True
        else:
            return False

    list_resource_classes_as_str.short_description = 'Class(es)'
    list_scopes_as_str.short_description = 'Scope(s)'
    list_solutions_as_str.short_description = 'Solution(s)'
    list_needs_as_str.short_description = 'Need(s)'
    is_project.short_description = 'Proj?'
    is_project.boolean = True
    is_organization.short_description = 'Org?'
    is_organization.boolean = True