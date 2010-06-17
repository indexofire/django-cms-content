# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class TinyMCEEditor(forms.Textarea):
    """
    TinyMCE widget. You can customize the configuration via tiny_mce_setup.js
    """
    class Media:
        js = (
            'admin/js/jquery.min.js',
            'cms_content/js/tiny_mce/tiny_mce.js',
            'cms_content/js/tiny_mce/tiny_mce_setup.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'tinymce'}
        if attrs:
            self.attrs.update(attrs)
        super(TinyMCEEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(TinyMCEEditor, self).render(name, value, attrs)
        return rendered
