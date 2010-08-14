# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language
from django.contrib.sites.models import Site

from menus.menu_pool import menu_pool
from menus.base import NavigationNode
from menus.menu_pool import MenuPool
from cms_content.models import CMSArticle


def cache_nodes(request, queryset):
    if queryset:
        lang = get_language()
        site_id = Site.objects.get_current().pk
        prefix = getattr(settings, "CMS_CACHE_PREFIX", "menu_cache_")
        key = "%smenu_nodes_%s_%s" % (prefix, lang, site_id)
        
        cached_nodes = cache.get(key, None)
        if cached_nodes:
            cached_nodes = str(cached_nodes)
            
        article_nodes = []
        for article in queryset:
            article_nodes.append(NavigationNode(
                article.title,
                article.url,
                article.menu.menuid,
                article.menu.parent,
                )
            )

        if str(article_nodes[0]) in cached_nodes:
            return

        nodes = menu_pool.get_nodes(request)
        for node in nodes:
            if node.title == article.category.slug:
                parent_node = node
                break
            else:
                parent_node = None

        for node in article_nodes:
            node.parent = parent_node
            if parent_node.namespace:
                node.namespace = parent_node.namespace
            nodes.append(node)

        duration = getattr(settings, "MENU_CACHE_DURATION", 60*60)
        cache.set(key, nodes, duration)
    else:
        return
