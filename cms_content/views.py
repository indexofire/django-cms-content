# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cms_content.models import CMSCategory

def categories(request, **kw):
    context = RequestContext(request, kw)
    return render_to_response("cms_content/index.html", context)

def category_view(request, id):
    return render_to_response('cms_content/category.html', RequestContext(request, {'category':CMSCategory.objects.get(pk=id)}))
