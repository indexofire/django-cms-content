# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from cms_content.models import *


urlpatterns = patterns ('cms_content.views',
    #show the default cms_content
    url(r'^$', 'content_index', name='content_index'),
    #show all of the sections table
    url(r'^section/$', 'section_list', name='section_list'),
    #show the categories list of the selected section
    url(r'^section/(?P<slug>[-\w]+)/$', 'section_detail', name='section_detail'),
    #show the articles list of the selected category
    url(r'^category/(?P<slug>[-\w]+)/$', 'category_detail', name='category_detail'),
    #show the article view
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'article_detail', name='article_detail'),
    url(r'^article/add/$', 'article_add', name='article_add'),
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/del/$', 'article_del', name='article_del'),
)
