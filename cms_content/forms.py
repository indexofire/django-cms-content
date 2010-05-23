# -*- coding: utf-8 -*-
from django import forms
from markitup.widgets import MarkItUpWidget
from cms_content.widgets import WYMEditor
from cms_content.models import CMSArticle

class CMSArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor(attrs={'cols': 80, 'rows': 120}))
    
    class Meta:
        model = CMSArticle
