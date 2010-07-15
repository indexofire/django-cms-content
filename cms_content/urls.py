# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from cms_content.models import *
from cms_content.utils.queryset import queryset_iterator


urlpatterns = patterns ('cms_content.views',
    url(r'^$', 'section_list', {'sections': CMSSection.objects.all()}, 
        name='section_list'),
    url(r'^add/$', 'article_add', name='article_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'category_list', name='category_list'),
    url(r'^(?P<slug>[-\w]+)/(?P<path>[-\w]+)/$', 'article_list', 
        name='article_list'),
    url(r'^(?P<slug>[-\w]+)/(?P<path>[-\w]+)/(?P<name>[-\w]+)/$', 
        'article_view', name='article_view'),
    url(r'^(?P<slug>[-\w]+)/(?P<path>[-\w]+)/(?P<name>[-\w]+)/delete/$', 
        'article_delete', name='article-delete'),
)
