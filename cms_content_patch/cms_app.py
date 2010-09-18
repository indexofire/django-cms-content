# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from cms_content.menu import CMSContentMenu


class CMSContentApp(CMSApp):
    name = _(u"CMS Content App")
    urls = ["cms_content.urls"]
    menus = [CMSContentMenu]

apphook_pool.register(CMSContentApp)
