# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

from cms_content.models import CMSMenuID
from cms_content.models import CMSSection
from cms_content.models import CMSCategory
from cms_content.models import CMSArticle
from cms_content.forms import CMSArticleAdminForm


__all__ = [
    'CMSArticleInline',
    'CMSCategoryInline',
    'CMSSectionAdmin',
    'CMSCategoryAdmin',
    'CMSArticleAdmin',
]

class CMSArticleInline(admin.StackedInline):
    """Article Inline Admin
    
    Create an article inline form to support add articles in category interface.
    """
    model = CMSArticle
    extra = 0
    verbose_name = _(u'Article Name')

class CMSCategoryInline(admin.StackedInline):
    """Category Inline Admin
    
    Create a category inline form to support add categories in section interface.
    """
    model = CMSCategory
    extra = 0
    verbose_name = _(u'Category Name')

class CMSSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    exclude = ('menu',)
    prepopulated_fields = {"slug": ("name",)}
    #inlines = [CMSCategoryInline,]
    
    def save_model(self, request, obj, form, change):
        if not change:
            menu_num = CMSMenuID.objects.count() + 1
            obj.menu = CMSMenuID.objects.create(
                menuid=menu_num,
                type='cmssection',
            )
            obj.save()
        else:
            obj.save()

class CMSCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'description')
    exclude = ('menu',)
    prepopulated_fields = {"slug": ("name",)}
    #inlines = [CMSArticleInline,]
    
    def save_model(self, request, obj, form, change):
        if not change:
            menu_num = CMSMenuID.objects.count() + 1
            obj.menu = CMSMenuID.objects.create(
                menuid=menu_num,
                parent=obj.section.menu.menuid,
                type='cmscategory',
            )
            obj.save()
        else:
            obj.menu = CMSMenuID.objects.get(menuid=obj.menu.menuid)
            obj.menu.parent = obj.section.menu.menuid
            obj.save()

class CMSArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_by',
        'category',
        'belong_to_section',
        'created_date',
        'last_modified_by',
        'last_modified_date',
        'pub_status',
    )
    list_filter = ('created_date', 'last_modified_date', 'pub_status')
    list_per_page = 20
    prepopulated_fields = {"slug": ("title",)}
    #list_display_links = ('title', )
    search_fields = ('title', 'content')
    #readonly_fields = ('title',)
    #list_editable = ('category',)
    actions = ['make_publish', 'make_draft', 'translate_content']
    form = CMSArticleAdminForm
    exclude = ('created_by', 'pub_start_date', 'pub_end_date', 'hits', 'menu', 'last_modified_by', 'last_modified_date')

    def belong_to_section(self, obj):
        return obj.category.section
    belong_to_section.short_description = 'section'

    def save_model(self, request, obj, form, change):
        if not change:
            # create a article
            menu_num = CMSMenuID.objects.count() + 1
            obj.menu = CMSMenuID.objects.create(
                menuid=menu_num,
                parent=obj.category.menu.menuid,
                type='cmsarticle',
            )
            obj.created_by = request.user
            obj.created_date = datetime.now()
            obj.save()
        else:
            # change the article
            obj.menu = CMSMenuID.objects.get(menuid=obj.menu.menuid)
            obj.menu.parent = obj.category.menu.menuid
            obj.last_modified_by = request.user
            obj.last_modified_date = datetime.now()
            obj.save()

    #def get_urls(self):
    #    urls = super(CMSArticleAdmin, self).get_urls()
    #    my_urls = patterns('',
    #        url(r'^(?P<slug>\w*)/(?P<path>\w*)/(?P<id>[0-9]+)/$', 
    #            article_view,
    #            name="article_view"),
    #    )
    #    return my_urls + urls

    def make_publish(self, request, queryset):
        """Mark Article Published
        
        Make selected articles to be published.
        """
        article_num = queryset.update(pub_status="pub")
        self.message_user(request,
            "%s article(s) marked as published!" % article_num
        )
    make_publish.short_description = _(u"Make the article published")
    
    def make_draft(self, request, queryset):
        """Mark Article as draft
        
        Make seclected articles to be draft.
        """
        article_num = queryset.update(pub_status="dra")
        self.message_user(request,
            "%s article(s) marked as draft!" % article_num
        )
    make_draft.short_description = _(u"Make the article as draft")


#class CMSMenuIDAdmin(admin.ModelAdmin):
#    list_display = ('menuid', 'parent', 'menu_entry')
#    list_per_page = 20


admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
#admin.site.register(CMSMenuID, CMSMenuIDAdmin)
