# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from cms_content.views import *
from cms_content.models import CMSSection, CMSCategory

section_info = {
    'queryset': CMSSection.objects.all(),
    'template_name': 'cms_content/section_list.html',
}

category_info = {
    'queryset': CMSCategory.objects.all(),
    'template_name': 'cms_content/category_list.html',
}

urlpatterns = patterns ('',
    url(r'^$', content_index, name='cms_content_index'),
    url(r'^section/$', list_detail.object_list, section_info, name='cms_content_section_list'),
    url(r'^category/$', list_detail.object_list, category_info, name='cms_content_category_list'),
    url(r'^section/(?P<slug>[-\w]+)/$', section_detail, name='cms_content_section_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$', category_detail, name='cms_content_category_detail'),
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', article_detail, name='cms_content_article_detail'),
    url(r'^article/add/$', article_add, name='cms_content_article_add'),
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/del/$', article_del, name='cms_content_article_del'),
)
