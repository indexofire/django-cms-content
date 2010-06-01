# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch

from cms.menu_bases import CMSAttachMenu
from cms.app_base import CMSApp
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool

from cms_content.models import CMSSection, CMSCategory, CMSArticle

class CMSSectionMenu(Menu):
    """CMS Section Menu
    Create a section list menu in pages.
    """
    #name = _("CMS Content")

    def get_nodes(self, request):
        nodes = []
        count = 1

        for section in CMSSection.objects.all():
            nodes.append(NavigationNode(section.name, '/cms/'+section.get_absolute_url(), section.pk))
            count += 1
            for category in CMSCategory.objects.select_related('section').filter(section__pk=section.pk):
                parent = count
                nodes.append(NavigationNode(category.name, '/cms/'+section.get_absolute_url()+category.get_absolute_url(), parent, category.section.pk))
                count += 1
                for article in CMSArticle.objects.select_related('category').filter(category__pk=category.pk):
                    nodes.append(NavigationNode(article.title, '/cms/'+section.get_absolute_url()+category.get_absolute_url()+article.get_absolute_url(), count, parent))
                    count += 1

        return nodes

class CMSCategoryMenu(Menu):
    """CMS Category Menu
    Create a category list menu in pages.
    """
    def get_nodes(self, request):
        nodes = []
        for cate in CMSCategory.objects.all():
            nodes.append(NavigationNode(cate.name, cate.get_absolute_url(), 'cmsplugin_category', cate.pk, cate.section, 'cmsplugin_category'))

        return nodes

menu_pool.register_menu(CMSSectionMenu)
menu_pool.register_menu(CMSCategoryMenu)
