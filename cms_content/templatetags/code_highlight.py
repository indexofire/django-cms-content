# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from cms_content.settings import *

from pygments import highlight
from pygments.lexers import guess_lexer, PythonLexer
from pygments.formatters import HtmlFormatter

from BeautifulSoup import BeautifulSoup


register = template.Library()

@register.filter(name='code_highlight')
@stringfilter
def code_highlight(content):
    if CODE_HIGHLIGHT:
        css = '''<link href="%scms_content/css/code_highlight.css"
            rel="stylesheet" type="text/css" />''' % settings.MEDIA_URL
        try:
            soup = BeautifulSoup(content)
            code_blocks = soup.findAll('pre')
            for code in code_blocks:
                try:
                    lexer = guess_lexer(code.string)
                except ValueError:
                    lexer = PythonLexer()
                format = HtmlFormatter(cssclass=CODE_HIGHLIGHT_CSS, linenos=CODE_HIGHLIGHT_LINENOS)
                code.replaceWith(highlight(code.string, lexer, format))
            return mark_safe(css + str(soup))
        except:
            return content
    else:
        return content
