"""Placeholder model for Zinnia"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField, PageField
from cms.plugin_rendering import render_placeholder

from zinnia.models import EntryAbstractClass
from django.template import Context

class EntryPlaceholder(EntryAbstractClass):
    """Entry with a Placeholder to edit content"""

    content_placeholder = PlaceholderField('content')
    #dm
    placeholder_render  = models.TextField(_('Placeholder render'), blank=True,null=True)
    page_link = PageField(verbose_name=_('page link'), null=True, blank=True)

    @property
    def html_content(self):
        """No additional formatting is necessary"""
        if self.placeholder_render:#dm
            return self.placeholder_render
        original = super(EntryPlaceholder,self).html_content
        return original

    class Meta(EntryAbstractClass.Meta):
        """EntryPlaceholder's Meta"""
        abstract = True
    #dm
    def get_absolute_url(self):
        """Return entry's URL"""
        if self.page_link:
            return self.page_link.get_absolute_url()
        else:
            return '/archivio/%s/%s/%s/%s' % (self.creation_date.strftime('%Y'),
                                          self.creation_date.strftime('%m'),
                                          self.creation_date.strftime('%d'),
                                          self.slug
        )
        #return super(EntryPlaceholder, self).get_absolute_url(self)