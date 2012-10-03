"""Admin of Zinnia CMS Plugins"""
from django.contrib import admin
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.plugin_rendering import render_placeholder
from cms.admin.placeholderadmin import PlaceholderAdmin
#dm
from cms.plugins.utils import get_plugins
from cms.plugin_rendering import render_plugins
from cms.utils.django_load import iterload_objects

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia.settings import ENTRY_BASE_MODEL


class EntryPlaceholderAdmin(PlaceholderAdmin, EntryAdmin):
    """EntryPlaceholder Admin"""
    fieldsets = ((None, {'fields': ('title', 'image', ('status','page_link'))}),
                 (_('Dates'), {'fields': ( ('event_timedate',  'end_publication'),
                                           ('start_publication', 'creation_date'),
                                         ),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Content'), {'fields': ('content_placeholder',),
                                 'classes': ('plugin-holder',
                                             'plugin-holder-nopage')}),
                 (_('Content Original'), {'fields': ('content',),
                                #'classes': ('collapse', 'collapse-open')
                                }),
                 (_('Options'), {'fields': ( 'featured',
                                            'excerpt', 'template',
                                            'related', 'authors',
#                                            'creation_date',
#                                            ('start_publication','end_publication')
                                            ),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Privacy'), {'fields': ('password', 'login_required',),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Discussion'), {'fields': ('comment_enabled',
                                               'pingback_enabled'),
                                    'classes': ('collapse', 'collapse-closed')}),
                 (_('Publication'), {'fields': ('sites', 'categories',
                                                'tags', 'slug')}))

    def save_model(self, request, entry, form, change):
        """Fill the content field with the interpretation
        of the placeholder"""
        context = RequestContext(request)
        #dm
        processors = iterload_objects(settings.CMS_PLUGIN_PROCESSORS)
        plugins = [plugin for plugin in get_plugins(request, entry.content_placeholder)]
        render = render_plugins(plugins, context, entry.content_placeholder)
        content = "".join(render)
        entry.placeholder_render = content
        #entry.placeholder_render = render_placeholder(entry.content_placeholder, context )
        #entry.content = render_placeholder(entry.content_placeholder, context)
        entry.save()
        super(EntryPlaceholderAdmin, self).save_model(
            request, entry, form, change)

    save_on_top = True
    #media = property(EntryAdmin.media)

if ENTRY_BASE_MODEL == 'cmsplugin_zinnia.placeholder.EntryPlaceholder':
    admin.site.unregister(Entry)
    admin.site.register(Entry, EntryPlaceholderAdmin)
