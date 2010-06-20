# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from pygments import highlight
from pygments.lexers import guess_lexer, PythonLexer
from pygments.formatters import HtmlFormatter
from BeautifulSoup import BeautifulSoup


register = template.Library()

@register.filter(name='pygmentize')
@stringfilter
def pygmentize(value):
    try:
        soup = BeautifulSoup(value)
        code_blocks = soup.findAll('pre')
        for code in code_blocks:
            try:
                lexer = guess_lexer(code.string)
            except ValueError:
                lexer = PythonLexer()
            format = HtmlFormatter(cssclass='code_highlight')
            code.replaceWith(highlight(code.string, lexer, format))
        return mark_safe(str(soup))
    except:
        return value
