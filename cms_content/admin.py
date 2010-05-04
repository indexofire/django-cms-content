# -*- coding: utf-8 -*-
from django.contrib import admin
from cms_content.models import CMSSection, CMSCategory, CMSArticle
from django.utils.translation import ugettext as _

class CMSSectionAdmin(admin.ModelAdmin):
    pass

class CMSCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    pass

class CMSArticleAdmin(admin.ModelAdmin):
    list_display = (_(u'title'), _(u'user'), _(u'category'), _(u'belong_to_section'), _(u'created'), _(u'modified'))
    list_filter = (_(u'created'), _(u'modified'))
    list_per_page = 20
    list_display_links = (_(u'title'), )
    #list_editable = ('category',)
    
    def belong_to_section(self, obj):
        article = CMSArticle.objects.select_related().get(pk=obj.id)
        return article.category.parent
    belong_to_section.short_description = _(u'section')

admin.site.register(CMSSection, CMSSectionAdmin)
admin.site.register(CMSCategory, CMSCategoryAdmin)
admin.site.register(CMSArticle, CMSArticleAdmin)
