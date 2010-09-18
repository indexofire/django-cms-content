# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode


class WYMEditor(forms.Textarea):
    """
    WYMEditor Widget For Admin Form.
    
    Introduction:
    WYMeditor is a web-based WYSIWYM XHTML editor. WYMeditor's main concept is 
    to leave details of the document's visual layout, and to concentrate on its 
    structure and meaning, while trying to give the user as much comfort as 
    possible.
    With WYMeditor, the code can't be contaminated by visual informations like 
    font styles and weights, borders, colors, ... 
    The end-user defines content meaning, which will determine its aspect by 
    the use of style sheets. The result is easy and quick maintenance of 
    information.
    See also: http://www.wymeditor.org/
    
    Usage:
    Copy or link media/cms_content to your project `MEDIA_ROOT` folder. The 
    widget will display in admin if you define `CMS_CONTENT_EDITOR = 'WYMEditor'`
    in your project's settings.py file.
    """
    class Media:
        js = (
            'admin/js/jquery.min.js',
            'cms_content/js/wymeditor/jquery.wymeditor.pack.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(WYMEditor, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            jQuery('#id_%s').wymeditor({
                updateSelector: '.submit-row input[type=submit]',
                updateEvent: 'click',
                skin: 'default',
                lang: '%s',
                postInitDialog: function (wym, wdw) {
                    wymeditor_filebrowser(wym, wdw);
                }
            });
            </script>''' % (name, self.language))


class TinyMCE(forms.Textarea):
    """
    TinyMCE Widget For Admin Form.
    
    Introduction:
    TinyMCE is a platform independent web based Javascript HTML WYSIWYG editor 
    control released as Open Source under LGPL by Moxiecode Systems AB. It has
    the ability to convert HTML TEXTAREA fields or other HTML elements to editor
    instances. TinyMCE is very easy to integrate into other Content Management
    Systems. 
    See also: http://tinymce.moxiecode.com/
    
    Usage:
    Copy or link media/cms_content to your project `MEDIA_ROOT` folder. The 
    widget will display in admin if you define `CMS_CONTENT_EDITOR = 'TinyMCE'`
    in project's settings.py file. The default value is 'WYMEditor'.
    
    You can customize your configuration in tiny_mce_setup.js. All configuration
    info was at http://wiki.moxiecode.com/index.php/TinyMCE:Configuration.
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
        super(TinyMCE, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(TinyMCE, self).render(name, value, attrs)
        return rendered


class MarkItUp(forms.Textarea):
    """
    MarkItUp Widget For Admin Form.

    Introduction:
    markItUp! is a JavaScript plugin built on the jQuery library. It allows you
    to turn any textarea into a markup editor. Html, Textile, Wiki Syntax,
    Markdown, BBcode or even your own Markup system can be easily implemented.
    See also: http://markitup.jaysalvat.com/

    Usage:
    Copy or link media/cms_content to your project `MEDIA_ROOT` folder. The 
    widget will display in admin if you define `CMS_CONTENT_EDITOR = 'MarkItUp'`
    in project's settings.py file. The default value is 'WYMEditor'.
    """
    class Media:
        js = (
            'admin/js/jquery.min.js',
            'cms_content/js/markitup/jquery.markitup.pack.js',
            'cms_content/js/markitup/sets/default/set.js',
        )
        css = {
            'all': (
                'cms_content/js/markitup/sets/default/style.css',
                'cms_content/js/markitup/skins/markitup/style.css',
            )
        }
    
    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'tinymce'}
        if attrs:
            self.attrs.update(attrs)
        super(MarkItUp, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(MarkItUp, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'''<script type="text/javascript" >
            $(document).ready(function() {
                $("#markItUp").markItUp(mySettings);
            });</script><textarea id="markItUp" class="markitup_editor" %s>%s
            </textarea>''' % (forms.util.flatatt(final_attrs),
            conditional_escape(force_unicode(value)))
        )
