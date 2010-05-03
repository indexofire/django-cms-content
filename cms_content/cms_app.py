# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from cms_content.menu import CMSCategoryMenu
from django.utils.translation import ugettext as _

class CMSCategory(CMSApp):
    name = _("CMS Category")
    urls = ["cms_content.urls"]
    menus = [CMSCategoryMenu]

apphook_pool.register(CMSCategory)
