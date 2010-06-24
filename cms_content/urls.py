# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from cms_content.views import *
from cms_content.models import *
from cms_content.utils.queryset import queryset_iterator


urlpatterns = patterns ('',
    url(r'^$', section_list, {'sections': CMSSection.objects.all()}, name='section'),
    url(r'^(?P<slug>\w*)/$', category_list, name='category_list'),
    url(r'^(?P<slug>\w*)/(?P<path>\w*)/$', article_list),
    url(r'^(?P<slug>[-\w]+)/(?P<path>[-\w]+)/(?P<name>[-\w]+)/$', article_view),
)
