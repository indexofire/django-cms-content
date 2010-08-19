# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models


def get_available_articles(queryset):
    """Get All Avaiable Articles
    
    """
    now = datetime.now()
    return queryset.filter(
        pub_status='pub',
        pub_start_date__lte=now,
        pub_end_date__gt=now,
    )

class CMSArticleManager(models.Manager):
    """Models CMSArticle Manager
    
    """
    def get_query_set(self):
        return get_available_articles(
            super(CMSArticleManager, self).get_query_set()
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
