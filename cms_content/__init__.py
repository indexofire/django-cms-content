# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse


models.Model._admin_url_name = lambda self, type: 'admin:%s_%s_%s' % (
    self._meta.app_label, self._meta.module_name, type)

def get_admin_change_url(self):
    return reverse(self._admin_url_name('change'), args=(self.pk,))
models.Model.get_admin_change_url = get_admin_change_url

def get_admin_delete_url(self):
    return reverse(self._admin_url_name('delete'), args=(self.pk,))
models.Model.get_admin_delete_url = get_admin_delete_url

def get_admin_history_url(self):
    return reverse(self._admin_url_name('history'), args=(self.pk,))
models.Model.get_admin_history_url = get_admin_history_url

def get_admin_changelist_url(self):
    return reverse(self._admin_url_name('changelist'))
models.Model.get_admin_changelist_url = get_admin_changelist_url

def get_admin_add_url(self):
    return reverse(self._admin_url_name('add'))
models.Model.get_admin_add_url = get_admin_add_url

models.Model.get_verbose_name = lambda self: self._meta.verbose_name
models.Model.get_verbose_name_plural = lambda self: self._meta.verbose_name_plural

VERSION = (0, 1, 'beta', 5)

def get_version(join=' ', short=False):
    """
    Return the version of this package as a string.

    The version number is built from a ``VERSION`` tuple, which should consist
    of integers, or trailing version information (such as 'alpha', 'beta' or
    'final'). For example:

    >>> VERSION = (2, 0, 6)
    >>> get_version()
    '2.0.6'

    >>> VERSION = (1, 0, 'beta', 2)
    >>> get_version()
    '1.0 beta 2'

    Use the ``join`` argument to join the version elements by an alternate
    character to the default ``' '``. This is useful when building a distutils
    setup module::

        from this_package import get_version

        setup(
            version=get_version(join='-'),
            # ...
        )

    Use the ``short`` argument to get the version number without trailing
    version information.

    """
    version = []
    number = []
    remainder = []
    for i, bit in enumerate(VERSION):
        if isinstance(bit, int):
            number.append(str(bit))
        else:
            remainder = [str(bit) for bit in VERSION[i:]] 
            break
    if number:
        version.append('.'.join(number))
    if not short:
        if remainder == ['alpha', 0]:
            version.append('pre-alpha')
        elif 'final' not in remainder:
            version.extend(remainder)
    return join.join(version)
