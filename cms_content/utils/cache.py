# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language
from django.contrib.sites.models import Site

from menus.menu_pool import menu_pool
from menus.base import NavigationNode

from cms_content.models import CMSArticle


def get_cache_key(lang=None, site=None, prefix='menu_cache'):
    """
    Determine cache key's prefix and surfix
    """
    lang = get_language()
    site = Site.objects.get_current().pk
    prefix = getattr(settings, 'CMS_CACHE_PREFIX', 'menu_cache')
    return '%s_menu_nodes_%s_%s' % (prefix, lang, site)
   

def get_or_set_cache(request, cache_key, model=CMSArticle, seconds_to_cache=60*30, **kwargs):
    """Cache key or get query

    Gets the query from cache or returns the queryset.

    Example:
    article = get_or_set_cache(key, CMSArticle, seconds_to_cache=60*30, slug='slug')

    """

    q = cache.get(cache_key)
    if not q:
        q = menu_pool.get_nodes(request)
        #cache.set(cache_key, q, seconds_to_cache)
    return q


def build_queryset_nodes(queryset=None):
    """Build the queryset's menu nodes

    Example:
    cache_node = queryset_nodes(qs)

    """
    nodes = []
    if queryset is None:
        return
    for node in queryset:
        nodes.append(NavigationNode(
            node.title,
            node.url,
            node.menu.menuid,
            node.menu.parent,
            )
        )
    return nodes


def category_node(article, nodes):
    """Get a category node which including queryset's articles
    
    Example:
    parent_node = category_node(article, nodes)
    
    """
    for node in nodes:
        if node.title == article.category.name:
            return node
    return None


def cache_nodes(request, qs):
    """Cache nodes from request
    
    Build a page of one category's article nodes
    
    Example:
    # in order to cache queryset's entries into cache, put this in your views
    # function.
    def view(request):
        queryset = Models.objects.filter("...")
        cache_nodes(queryset)
        ...
    
    """
    if qs:
        parent_node = None
        key = get_cache_key()

        # build article_nodes from queryset in menu cache
        article_nodes = build_queryset_nodes(qs)

        # get the original cache nodes. if blank, get the whole nodes. if
        # article_nodes are already in cache nodes, return.
        #cached_nodes = cache.get(key, None)
        cached_nodes = get_or_set_cache(request, key)
        for i in cached_nodes:
            print "cached_node:", i, i.title, i.id, i.parent_id, i.namespace, i.parent
        if cached_nodes:
            str_cached_nodes = str(cached_nodes)
            if str(article_nodes[0]) in str_cached_nodes:
                return

        parent_node = category_node(qs[0], cached_nodes)
        print parent_node
        # add parent_node to the article node and save into cached_node
        for node in article_nodes:
            node.parent = parent_node
            node.namespace = getattr(parent_node, 'namespace', None)
            cached_nodes.append(node)

        duration = getattr(settings, "MENU_CACHE_DURATION", 60*60)
        cache.set(key, cached_nodes, duration)
    else:
        return
