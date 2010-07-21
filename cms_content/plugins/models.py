# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

from cms_content.models import CMSCategory


TEMPLATES = [
    ('cms_content/plugins/latest_article.html', 'latest articles'),
    ('cms_content/plugins/tophit_article.html', 'tophit articles'),
]

class LatestArticle(CMSPlugin):
    """
    This model will save latest articles' id for plugin
    """

    category = models.ManyToManyField(CMSCategory, verbose_name=_('category'))
    author = models.ManyToManyField(User, verbose_name=_('authors'))
    article_num = models.IntegerField(_(u'number of articles'), default=5)
    template = models.CharField(_(u'template'), blank=True, max_length=250, 
        choices=TEMPLATES, default='latest articles',
        help_text=_(u'Template used to display the plugin'))

    def __unicode__(self):
        return _(u'%d articles') % self.article_num

    @property
    def render_template(self):
        return self.template

class TopHitArticle(CMSPlugin):
    """
    This model will save top hits articles's id for plugin
    """
    
    category = models.ManyToManyField(CMSCategory, verbose_name=_(u'category'))
    author = models.ManyToManyField(User, verbose_name=_(u'authors'))
    article_num = models.IntegerField(_(u'number of articles'), default=5)
    template = models.CharField(_(u'template'), blank=True, max_length=250,
        choices=TEMPLATES, default='tophit articles',
        help_text=_(u'Template used to display the plugin'))
    
    def __unicode__(self):
        return _(u'%d articles') % self.article_num
    
    @property
    def render_template(self):
        return self.template
