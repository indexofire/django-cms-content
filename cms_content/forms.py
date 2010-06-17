# -*- coding: utf-8 -*-
from django import forms
from cms_content.widgets.wymeditor import WYMEditor
from cms_content.widgets.tinymce import TinyMCEEditor
from cms_content.models import CMSArticle

class CMSArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=WYMEditor(attrs={'cols': 80, 'rows': 40}))
    
    class Meta:
        model = CMSArticle
