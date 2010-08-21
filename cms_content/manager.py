# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_pub_articles(queryset):
    """Get All Avaiable Articles
    
    """
    now = datetime.now()
    STATUS = 'pub'

    return queryset.filter(
        pub_status=STATUS,
        pub_start_date__lte=now,
        pub_end_date__gt=now,
    )

def get_del_articles(queryset):
    """Get All Avaiable Articles
    
    """
    STATUS = DEL
    return queryset.filter(
        pub_status=STATUS
    )


class CMSArticlePubManager(models.Manager):
    """Models CMSArticle Manager
    
    """
    def get_query_set(self):
        return get_pub_articles(
            super(CMSArticlePubManager, self).get_query_set()
        )
    
    def search(self, pattern):
        lookup = None
        for pattern in pattern.split():
            q = models.Q(content__icontains=pattern) | models.Q(title__icontains=pattern)
            if lookup is None:
                lookup = q
            else:
                lookup |= q
        return self.get_query_set().filter(lookup)
