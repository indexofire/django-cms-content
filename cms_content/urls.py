# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from cms_content.views import *

urlpatterns = patterns ('',
    url(r'^$', content_index, name='cms_content_index'),
    url(r'^section/$', section_list, name='cms_content_section_list'),
    url(r'^section/(?P<slug>[-\w]+)/$', section_detail, name='cms_content_section_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$', category_detail, name='cms_content_category_detail'),
    url(r'^article/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[-\w]+)/$', article_detail, name='cms_content_article_detail'),
    url(r'^article/add/$', article_add, name='cms_content_article_add'),
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/del/$', article_del, name='cms_content_article_del'),
)
