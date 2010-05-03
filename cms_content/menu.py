# -*- coding: utf-8 -*-
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch

from cms.menu_bases import CMSAttachMenu
from cms.app_base import CMSApp
from cms_content.models import CMSCategory

class CMSCategoryMenu(Menu):
    """
    Create a category list menu in pages.
    """
    def get_nodes(self, request):
        nodes = []
        for cate in CMSCategory.objects.all():
            nodes.append(NavigationNode(cate.name, cate.get_absolute_url(), 'cmsplugin_category', cate.pk, cate.parent_id, 'cmsplugin_category'))

        return nodes

menu_pool.register_menu(CMSCategoryMenu)
