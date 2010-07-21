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
        articles = list(CMSArticle.objects.all().select_related(depth=1))
        
        for section in sections:
            url = ROOT_URL + 'section/' + section.url
            nodes.append(NavigationNode(section.name, url, section.menu.menuid))
        for category in categories:
            url = ROOT_URL + 'category/' + category.url
            nodes.append(NavigationNode(category.name, url, category.menu.menuid, category.menu.parent))
        for article in articles:
            url = ROOT_URL + 'article/' + article.url
            nodes.append(NavigationNode(article.title, url, article.menu.menuid, article.menu.parent))
        return nodes


menu_pool.register_menu(CMSContentMenu)
