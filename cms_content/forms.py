# -*- coding: utf-8 -*-
from django import forms

from cms_content.settings import EDITOR
from cms_content.models import CMSArticle
from cms_content import widgets


class CMSArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=getattr(widgets, EDITOR))
    
    class Meta:
        model = CMSArticle
