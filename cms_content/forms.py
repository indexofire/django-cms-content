# -*- coding: utf-8 -*-
from django import forms

from cms_content.settings import EDITOR
from cms_content.models import CMSArticle
from cms_content import widgets


WIDGET = getattr(widgets, EDITOR)

class CMSArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=WIDGET)
    
    class Meta:
        model = CMSArticle

class CMSArticleFrontendForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    content = forms.CharField(widget=WIDGET)
    
    class Meta:
        model = CMSArticle
        fields = ('title', 'slug', 'content', 'category',)
