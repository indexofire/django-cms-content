# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django import forms
from django.utils.translation import ugettext as _
from cms_content.models import CMSSection, CMSCategory, CMSArticle
from cms_content.forms import CMSArticleAdminForm

class CMSSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('created', 'modified')
    pass

class CMSCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('created', 'modified')
    pass

class CMSArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'belong_to_section', 'created', 'modified')
    list_filter = ('created', 'modified')
    list_per_page = 20
    list_display_links = ('title', )
    search_fields = ('title', 'user')
    #list_editable = ('category',)
    
    forms = CMSArticleAdminForm
    
    def belong_to_section(self, obj):
        article = CMSArticle.objects.select_related().get(pk=obj.id)
        return article.category.section
    belong_to_section.short_description = 'section'



admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
