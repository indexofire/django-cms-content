# -*- coding: utf-8 -*-
from django import forms

from cms_content.settings import EDITOR
from cms_content.models import *
from cms_content import widgets


class CMSArticleAdminForm(forms.ModelForm):
    widget = getattr(widgets, EDITOR)
    content = forms.CharField(widget=widget)
    
    class Meta:
        model = CMSArticle

class CMSArticleFrontendForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = CMSArticle
        fields = ('title', 'slug', 'content', 'category')
