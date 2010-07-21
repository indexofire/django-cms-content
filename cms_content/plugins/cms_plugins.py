# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cms_content.models import CMSArticle
from cms_content.plugins.models import LatestArticle
from cms_content.settings import ROOT_URL


class LatestArticlePlugin(CMSPluginBase):
    """
    This Plugin will get latest articles.
    """
    model = LatestArticle
    name = _('Latest Article')
    render_template = 'cms_content/plugins/latest_article.html'
    
    def render(self, context, instance, placeholder):
        articles = CMSArticle.objects.filter()[:instance.article_num]
        context.update({
            'articles': articles,
            'object': instance,
            'placeholder': placeholder,
            }
        )
        return context

plugin_pool.register_plugin(LatestArticlePlugin)
