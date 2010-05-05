# -*- coding: utf-8 -*-
from django import forms
from cms.plugins.text.widgets.wymeditor_widget import WYMEditor

from cms_content.models import CMSArticle

class CMSArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor(attrs={'cols': 80, 'rows': 40}))
    
    class Meta:
        model = CMSArticle
