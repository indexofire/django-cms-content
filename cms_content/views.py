# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponseRedirect
from django.db.models import F
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from cms_content.models import *
from cms_content.utils.render import render_to
from cms_content.forms import CMSArticleFrontendForm
from cms_content.settings import ROOT_URL, ARTICLE_PERPAGE
from cms_content.menu_nodes import cache_nodes

@render_to('cms_content/content_index.html')
def content_index(request):
    articles = CMSArticle.objects.all()[:10]
    return {
        'articles': articles,
    }

#@cache_page(60*30)
@render_to('cms_content/section_list.html')
def section_list(request):
    #request_page = request.GET.get('page', 1)
    sections = list(CMSSection.objects.all())
    #paginator = Paginator(sections, 10)
    return {
        'sections': sections,
        #'paginator': paginator,
        #'page': paginator.page(request_page), # add 1 query
    }

#@cache_page(60*30)
@render_to('cms_content/section_detail.html')
def section_detail(request, slug):
    #request_page = request.GET.get('page', 1)
    section = CMSSection.objects.get(slug=slug) # add 1 query
    categories = CMSCategory.objects.select_related(depth=1).filter(section=section) # add 0 query
    #paginator = Paginator(categories, CATEGORY_PERPAGE) # add 0 query
    return {
        #'page': paginator.page(request_page), # add 1 query
        #'paginator': paginator,
        #'request_page': int(request_page),
        'section': section,
        'categories': categories,
    }

@render_to('cms_content/category_detail.html')
def category_detail(request, slug):
    """View of list articles of category with name slug
    
    """
    category = CMSCategory.objects.select_related(depth=1).get(slug=slug)
    articles = list(CMSArticle.objects.select_related(depth=1).\
        filter(category=category).filter(pub_status="pub"))
    paginator = Paginator(articles, ARTICLE_PERPAGE)
    try:
        request_page = int(request.GET.get('page', 1))
    except ValueError:
        request_page = 1
    try:
        article_page = paginator.page(request_page)
        queryset = articles[(request_page-1)*ARTICLE_PERPAGE:request_page*ARTICLE_PERPAGE]
    except (EmptyPage, InvalidPage):
        article_page = paginator.page(paginator.num_pages)
        queryset = articles[(paginator.num_pages-1)*ARTICLE_PERPAGE:paginator.num_pages*ARTICLE_PERPAGE]
    cache_nodes(request, queryset)
    return {
        'pages': article_page,
        #'paginator': paginator,
        #'request_page': request_page,
        'section': category.section,
        'category': category,
        'articles': queryset,
    }

@render_to('cms_content/article_detail.html')
def article_detail(request, year, month, day, slug):
    article = CMSArticle.objects.select_related(depth=2).get(slug=slug)
    article.hits = F('hits') + 1
    article.save()
    return {
        'section': article.category.section,
        'category': article.category,
        'article': article,
    }

@login_required
@render_to('cms_content/article_add.html')
def article_add(request):
    if request.method=="POST":
        form = CMSArticleFrontendForm(request.POST)
        if form.is_valid():
            article = CMSArticle.objects.create(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'], 
                slug = form.cleaned_data['slug'], 
                category = form.cleaned_data['category'],
                created_by = request.user,
                created_date = datetime.now(),
                last_modified_by = request.user,
                last_modified_date = datetime.now(),
                pub_status = 'pub',
                menu = form.cleaned_data['menu'],
            )
            article.save()
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError('Error')
        return HttpResponseRedirect(ROOT_URL)
    else:
        article_form = CMSArticleFrontendForm(
            initial={'title':'your article title'},
        )
        return {
            'form': article_form,
            'request': request,
        }

def article_del(request, slug, path, name):
    if request.user.is_superuser:
        article = CMSArticle.objects.get(slug=name)
        article.delete()
        return HttpResponseRedirect(ROOT_URL)
