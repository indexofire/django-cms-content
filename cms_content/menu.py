# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from cms.menu_bases import CMSAttachMenu

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
        nodes=[]
        count = 1
        sections = CMSSection.objects.all()
        for section in sections:
            url = settings.ROOT_URL + section.get_absolute_url()
            nodes.append(NavigationNode(section.name, url, section.pk))
            count += 1
            categories = CMSCategory.objects.select_related('section').filter(section__pk=section.pk)
            for category in categories:
                url = url + category.get_absolute_url()
                parent = count
                nodes.append(NavigationNode(category.name, url, parent, category.section_id))
                count += 1
                articles = CMSArticle.objects.select_related('category').filter(category__pk=category.pk)
                for article in articles:
                    url = url + article.get_absolute_url()
                    nodes.append(NavigationNode(article.title, url, count, parent))
                    count += 1
        return nodes


menu_pool.register_menu(CMSSectionMenu)
