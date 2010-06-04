# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from cms_content.models import CMSSection, CMSCategory, CMSArticle
from cms_content.forms import CMSArticleAdminForm
from cms_content.views import article_view
from datetime import datetime
from cms_content.glanguage import Translator

class CMSArticleInline(admin.StackedInline):
    """Article Inline
    Create an article inline form to support add articles in category interface.
    """
    model = CMSArticle
    extra = 0
    verbose_name = _(u'Article Name')

class CMSCategoryInline(admin.StackedInline):
    """Category Inline
    Create a category inline form to support add categories in section interface.
    """
    model = CMSCategory
    extra = 0
    verbose_name = _(u'Category Name')

class CMSSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('created', 'modified')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CMSCategoryInline,]

class CMSCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('created', 'modified')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CMSArticleInline,]

class CMSArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'belong_to_section', 'created_date', 'last_modified_by', 'last_modified_date', 'is_published')
    list_filter = ('created_date', 'last_modified_date', 'is_published')
    list_per_page = 20
    prepopulated_fields = {"slug": ("title",)}
    #list_display_links = ('title', )
    search_fields = ('title', 'content')
    #readonly_fields = ('user',)
    #list_editable = ('category',)
    actions = ['make_publish', 'translate_content']
    form = CMSArticleAdminForm

    def belong_to_section(self, obj):
        article = CMSArticle.objects.select_related().get(pk=obj.id)
        return article.category.section
    belong_to_section.short_description = 'section'

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
            obj.last_modified_date = datetime.now()
        obj.save()

    def get_urls(self):
        urls = super(CMSArticleAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^article/$', article_view, name="article_view"),
        )
        return my_urls + urls

    def make_publish(self, request, queryset):
        article_num = queryset.update(is_published = True)
        self.message_user(request, "%s article(s) marked as published!" % article_num)
    make_publish.short_description = _(u"Make the article published")

    def translate_content(self, request, queryset):
        self.message_user(request, "The article(s) had been translated!")
        pass
    translate_content.short_description = _(u"Translate the article")

admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
