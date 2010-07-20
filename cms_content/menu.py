# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from cms_content.settings import ROOT_URL
from cms_content.models import CMSSection, CMSCategory, CMSArticle

            
class CMSContentMenu(CMSAttachMenu):
    """CMS Content Menu
    
    Append a cms_content menu list in pages.
    """
    name = _("CMS Content Menu")

    def get_nodes(self, request):
        nodes=[]
        sections = CMSSection.objects.all()
        count = sections.count() + 1
        sections = list(sections)
        for section in sections:
            url = 'cms'
            nodes.append(NavigationNode(section.name, url, section.pk))
            categories = CMSCategory.objects.select_related('section').filter(section__pk=section.pk)
            for category in categories:
                url = "cms"
                parent = count
                nodes.append(NavigationNode(category.name, url, parent, 1))
                count += 1
                articles = CMSArticle.objects.select_related('category').filter(category__pk=category.pk)
                for article in articles:
                    url = "cms"
                    nodes.append(NavigationNode(article.title, url, count, parent))
                    count += 1
        for node in nodes:
            print node
        return nodes


menu_pool.register_menu(CMSContentMenu)
