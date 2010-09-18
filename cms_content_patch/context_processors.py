# -*- coding: utf-8 -*-
from django.conf import settings

def content_page(request):
    """
    add content root page url
    """
    return {'CMS_ROOT_PAGE': settings.CMS_CONTENT_ROOT_URL}
