from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

JQUERY_URL = getattr(settings,'WYMEDITOR_JQUERY_URL','cms_content/js/jquery.js')
JS_URL = getattr(settings,'WYMEDITOR_JS_URL','cms_content/js/wymeditor/')

class WYMEditor(forms.Textarea):
    class Media:
        js = (
            #'%s' % JQUERY_URL,
            'admin/js/jquery.min.js',
            '%sjquery.wymeditor.pack.js' % JS_URL,
            #'%splugins/jquery.wymeditor.filebrowser.js' % JS_URL,
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
                lang: '%s',
                postInitDialog: function (wym, wdw) {
                    wymeditor_filebrowser(wym, wdw);
                }
            });
            </script>''' % (name, self.language))

