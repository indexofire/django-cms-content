# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from cms_content.views import *
from cms_content.models import *

urlpatterns = patterns ('',
    url(r'^$', sections, {'sections': CMSSection.objects.all()}, name='section'),
    #url(r'^category/$', categories, {'message': 'sample root page', 'category': CMSCategory.objects.all()}, name='category_index'),
    url(r'^(?P<slug>\w*)/$', category_view, name='category_view'),
    url(r'^(?P<slug>\w*)/(?P<path>\w*)/$', article_list),
    url(r'^(?P<slug>\w*)/(?P<path>\w*)/(?P<name>[\w-]*)/$', article_view),
)
