# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from cms_content.models import CMSSection, CMSCategory, CMSArticle
from cms_content.utils import render_to

def categories(request, **kw):
    context = RequestContext(request, kw)
    return render_to_response("cms_content/index.html", context)

def category_view(request, id):
    return render_to_response('cms_content/category.html', RequestContext(request, {'category':CMSCategory.objects.get(pk=id)}))


@login_required
@render_to('article_list.html')
def article_list(request, article_slug):
    request_page = request.GET.get('page', 1)
    article = get_object_or_404(CMSSection, slug=article_slug)
    queryset = CMSArticle.objects.user_objects(request.user).filter(forum=forum)
    paginator = Paginator(queryset, 50)
    return response(request, 'forum/thread_list.html', {'page': paginator.page(request_page), 'paginator': paginator, 'request_page': int(request_page), 'forum': forum })
