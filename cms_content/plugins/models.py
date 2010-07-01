# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

from cms_content.models import CMSCategory


TEMPLATES = [('cms_content/plugins/latest_article.html', 'article list')]

class LatestArticle(CMSPlugin):
    """
    This model will save latest articles' id
    """
    #latest_num = 
    category = models.ForeignKey(CMSCategory, verbose_name=_('category'))
    author = models.ForeignKey(User, verbose_name=_('authors'))
    article_num = models.IntegerField(_('number of article'), default=5)
    template = models.CharField(_('template'), blank=True, max_length=250, 
        choices=TEMPLATES, help_text=_('Template used to display the plugin'))

    def __unicode__(self):
        return _('%s articles') % self.article_num

    @property
    def render_template(self):
        return self.template
