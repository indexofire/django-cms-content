# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from cms_content.settings import ROOT_URL
from cms_content.models import CMSMenuID, CMSSection, CMSCategory, CMSArticle


class CMSContentMenu(CMSAttachMenu):
    """CMS Content Menu
    
    Append cms_content menu into cms menu.
    """
    
    name = _(u"CMS Content Menu")
    
    def get_nodes(self, request):
        nodes = []
        sections = list(CMSSection.objects.all().select_related(depth=1))
        categories = list(CMSCategory.objects.all().select_related(depth=1))
        #articles = list(CMSArticle.objects.all()[:2].select_related(depth=1))
        
        for section in sections:
            nodes.append(NavigationNode(
                section.name,
                section.url,
                section.menu.menuid,
                )
            )
        for category in categories:
            nodes.append(NavigationNode(
                category.name,
                category.url,
                category.menu.menuid,
                category.menu.parent,
                )
            )
        #for article in articles:
        #    nodes.append(NavigationNode(
        #        article.title,
        #        article.url,
        #        article.menu.menuid,
        #        article.menu.parent,
        #        )
        #    )
        return nodes


menu_pool.register_menu(CMSContentMenu)
