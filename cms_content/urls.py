# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from cms_content.views import sections, section_view, categories, category_view
from cms_content.models import CMSSection, CMSCategory

urlpatterns = patterns ('',
    url(r'^$', sections, {'sections': CMSSection.objects.all()}, name='section'),
    url(r'^category/$', categories, {'message': 'sample root page', 'category': CMSCategory.objects.all()}, name='category_index'),
    url(r'^(?P<path>.*)/$', category_view, name='category_view'),
    #url(r'^(?P<id>[0-9]+)/$', section_view, name='section'),
)
