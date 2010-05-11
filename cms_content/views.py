# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from cms_content.models import CMSSection, CMSCategory, CMSArticle
from cms_content.utils import render_to

def sections(request, **kw):
    context = RequestContext(request, kw)
    return render_to_response("cms_content/index.html", context)

def categories(request, **kw):
    context = RequestContext(request, kw)
    return render_to_response("cms_content/category_index.html", context)

#def category_view(request, path):
#    return render_to_response('cms_content/category_list.html', RequestContext(request, {'category': CMSCategory.objects.get(section=path)}))

def section_view(request, *args):
    return render_to_response('cms_content/section.html', RequestContext(request, {'section': CMSSection.objects.get(pk=id)}))

@render_to('cms_content/category_list.html')
def category_view(request, category_slug):
    request_page = request.GET.get('page', 1)
    category = get_object_or_404(CMSSection, slug=category_slug)
    queryset = CMSCategory.objects.filter(name=category)
    paginator = Paginator(queryset, 50)
    return response(request, {'page': paginator.page(request_page), 'paginator': paginator, 'request_page': int(request_page), 'category': category})


@login_required
@render_to('article_list.html')
def article_list(request, article_slug):
    request_page = request.GET.get('page', 1)
    article = get_object_or_404(CMSSection, slug=article_slug)
    queryset = CMSArticle.objects.user_objects(request.user).filter(forum=forum)
    paginator = Paginator(queryset, 50)
    return response(request, 'cms_content/article_list.html', {'page': paginator.page(request_page), 'paginator': paginator, 'request_page': int(request_page), 'forum': forum })
