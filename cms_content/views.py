# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from cms_content.models import *
from cms_content.utils.render import render_to


def section_list(request, **kw):
    context = RequestContext(request, kw)
    return render_to_response("cms_content/section_list.html", context)

@render_to('cms_content/category_list.html')
def category_list(request, slug):
    request_page = request.GET.get('page', 1)
    section = get_object_or_404(CMSSection, slug=slug)
    queryset = CMSCategory.objects.filter(section=section)
    paginator = Paginator(queryset, 10)
    return {'page': paginator.page(request_page),
        'paginator': paginator,
        'request_page': int(request_page),
        'section': section,
        'category_list': queryset,
    }

@render_to('cms_content/article_list.html')
def article_list(request, slug, path):
    request_page = request.GET.get('page', 1)
    section = get_object_or_404(CMSSection, slug=slug)
    category = get_object_or_404(CMSCategory, slug=path)
    queryset = CMSArticle.objects.filter(category=category).exclude(is_published=False)
    paginator = Paginator(queryset, 10)
    return {'page': paginator.page(request_page),
        'paginator': paginator,
        'request_page': int(request_page),
        'category': category,
        'section': section,
        'article_list': queryset,
    }

@render_to('cms_content/article.html')
def article_view(request, slug, path, name):
    section = get_object_or_404(CMSSection, slug=slug)
    category = get_object_or_404(CMSCategory, slug=path)
    queryset = CMSArticle.objects.get(slug=name)
    return {'category': category,
        'section': section,
        'article': queryset,
    }
