# -*- coding: utf-8 -*-
from django.contrib import admin
from cms_content.models import CMSSection, CMSCategory, CMSArticle

class CMSSectionAdmin(admin.ModelAdmin):
    pass

class CMSCategoryAdmin(admin.ModelAdmin):
    pass

class CMSArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'modified'
    pass

admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
