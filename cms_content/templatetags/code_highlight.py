# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter

from cms_content.settings import *

from pygments import highlight
from pygments.lexers import guess_lexer, PythonLexer, LEXERS, get_lexer_by_name
from pygments.formatters import HtmlFormatter

from BeautifulSoup import BeautifulSoup


register = template.Library()

@register.filter(name='code_highlight')
@stringfilter
def code_highlight(content):
    if CODE_HIGHLIGHT:
        if CODE_HIGHLIGHT_LINENOS:
            css = u'''<link href="%scms_content/css/code_highlight_table.css"
                rel="stylesheet" type="text/css" />''' % settings.MEDIA_URL
        else:
            css = u'''<link href="%scms_content/css/code_highlight_div.css"
                rel="stylesheet" type="text/css" />''' % settings.MEDIA_URL
        try:
            soup = BeautifulSoup(content)
            code_blocks = soup.findAll(u'pre')
            for code in code_blocks: 
                if code.has_key(u'class'):
                    lang = code[u'class']
                    if lang not in reduce(lambda a,b: a + b[2], 
                        LEXERS.itervalues(), ()):
                        lang = CODE_HIGHLIGHT_DEFAULT
                    lexer = get_lexer_by_name(lang, stripall=True, 
                        encoding=u'UTF-8')
                else:
                    try:
                        lexer = guess_lexer(code.string)
                    except ValueError:
                        lexer = PythonLexer
                format = HtmlFormatter(cssclass=CODE_HIGHLIGHT_CSS, 
                    linenos=CODE_HIGHLIGHT_LINENOS)
                code.replaceWith(highlight(code.string, lexer, format))
            return mark_safe(css + force_unicode(soup).replace('&amp;', '&'))
        except:
            return content
    else:
        return content
