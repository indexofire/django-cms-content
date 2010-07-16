# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from cms_content.menu import CMSSectionMenu


class CMSSection(CMSApp):
    name = _(u"CMS Section")
    urls = ["cms_content.urls"]
    menus = [CMSSectionMenu]

apphook_pool.register(CMSSection)
