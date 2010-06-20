# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.core.urlresolvers import NoReverseMatch

from cms.menu_bases import CMSAttachMenu
from cms.app_base import CMSApp

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from cms_content import settings
from cms_content.models import *


class CMSSectionMenu(CMSAttachMenu):
    """
    CMS Section Menu
    Create a section list menu in pages.
    """
    name = _("CMS Content Menu")

    def get_nodes(self, request):
        nodes = []
        count = 1
        sections = CMSSection.objects.all()

        for section in sections:
            nodes.append(NavigationNode(section.name,
                settings.CMS_CONTENT_URL+section.get_absolute_url(),
                section.pk)
            )
            count += 1
            categories = CMSCategory.objects.select_related('section').filter(section__pk=section.pk)
            for category in categories:
                parent = count
                nodes.append(NavigationNode(category.name,
                    settings.CMS_CONTENT_URL+section.get_absolute_url()+category.get_absolute_url(),
                    parent,
                    category.section.pk)
                )
                count += 1
                articles = CMSArticle.objects.select_related('category').filter(category__pk=category.pk).iterator()
                for article in articles:
                    nodes.append(NavigationNode(article.title,
                        settings.CMS_CONTENT_URL+section.get_absolute_url()+category.get_absolute_url()+article.get_absolute_url(),
                        count,
                        parent)
                    )
                    count += 1
        return nodes

menu_pool.register_menu(CMSSectionMenu)
