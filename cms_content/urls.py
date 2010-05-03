# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from cms_content.views import categories, category_view
from cms_content.models import CMSCategory

urlpatterns = patterns ('',
    url(r'^$', categories, {'message': 'sample root page', 'category': CMSCategory.objects.all()}, name='category_index'),
    url(r'^(?P<id>[0-9]+)/$', category_view, name='category_view'),
)
