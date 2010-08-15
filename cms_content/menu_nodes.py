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
    """
    Build a page of one category's article nodes
    """
    if queryset:
        lang = get_language()
        site_id = Site.objects.get_current().pk
        prefix = getattr(settings, "CMS_CACHE_PREFIX", "menu_cache_")
        key = "%smenu_nodes_%s_%s" % (prefix, lang, site_id)
        parent_node = None

        # build article_nodes from queryset in menu cache
        article_nodes = []
        for article in queryset:
            article_nodes.append(NavigationNode(
                article.title,
                article.url,
                article.menu.menuid,
                article.menu.parent,
                )
            )

        # get the original cache nodes. if blank, get the whole nodes. if
        # article_nodes are already in cache nodes, return.
        cached_nodes = cache.get(key, None)
        if cached_nodes:
            cached_nodes = str(cached_nodes)
            if str(article_nodes[0]) in cached_nodes:
                return
            for node in cached_nodes:
                if node.namespace == 'CMSContentMenu':
                    if node.title == article.category.slug:
                        parent_node = node
                        break
                else:
                    parent_node = None
        else:
            cached_nodes = menu_pool.get_nodes(request)

        # add parent_node to the article node and save into cached_node
        for node in article_nodes:
            node.parent = parent_node
            node.namespace = getattr(parent_node, 'namespace', None)
            cached_nodes.append(node)

        duration = getattr(settings, "MENU_CACHE_DURATION", 60*60)
        cache.set(key, cached_nodes, duration)
    else:
        return
