# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.site.models import Site

from cms_content.models import CMSArticle

def get_available_articles(queryset):
    """Get All Avaiable Articles
    
    """
    now = datetime.now()
    return queryset.filter(
        status=PUBLISHED,
        publish_start_date__lte=now,
        publish_end_date__gt=now,
        sites=Site.objects.get_current(),
    )

class CMSArticleManager(models.Manager):
    """Models CMSArticle Manager
    
    """
    def get_queryset(self):
        return get_available_articles(
            super(CMSArticleManager, self).getqueryset()
        )
    
    def search(self, pattern):
        lookup = None
        for pattern in pattern.split():
            q = models.Q(content__icontains=pattern) | models.Q(title__icontains=pattern)
            if lookup is None:
                lookup = q
            else:
                lookup |= q
        return self.get_queryset().filter(lookup)
