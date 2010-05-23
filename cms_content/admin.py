# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django import forms
from django.utils.translation import ugettext as _
from cms_content.models import CMSSection, CMSCategory, CMSArticle
from cms_content.forms import CMSArticleAdminForm

class CMSArticleInline(admin.StackedInline):
    model = CMSArticle
    extra = 0
    verbose_name = _(u'Article Name')

class CMSCategoryInline(admin.StackedInline):
    model = CMSCategory
    extra = 0
    verbose_name = _(u'Category Name')

class CMSSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('created', 'modified')
    inlines = [
        CMSCategoryInline,
    ]

class CMSCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('created', 'modified')
    inlines = [
        CMSArticleInline,
    ]

class CMSArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'belong_to_section', 'created', 'modified')
    list_filter = ('created', 'modified')
    list_per_page = 20
    #list_display_links = ('title', )
    search_fields = ('title', 'user')
    #readonly_fields = ('user',)
    #list_editable = ('category',)
    form = CMSArticleAdminForm
    
    def belong_to_section(self, obj):
        article = CMSArticle.objects.select_related().get(pk=obj.id)
        return article.category.section
    belong_to_section.short_description = 'section'
    
    #def article_author(self, obj):
        



admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
