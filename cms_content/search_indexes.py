# -*- coding: utf-8 -*-
import datetime

from haystack.indexes import *
from haystack import site

from cms_content.models import CMSArticle


class CMSArticleIndex(SearchIndex):
    text = CharField(document=True)
    author = CharField(model_attr='created_by')
    pub_date = DateTimeField(model_attr='created_date')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return CMSArticle.objects.filter(created_date__lte=datetime.datetime.now())


site.register(CMSArticle, CMSArticleIndex)
