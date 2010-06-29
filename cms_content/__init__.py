from django.db import models
from django.core.urlresolvers import reverse

models.Model._admin_url_name = lambda self, type: 'admin:%s_%s_%s' % (
    self._meta.app_label, self._meta.module_name, type)

def get_admin_change_url(self):
    return reverse(self._admin_url_name('change'), args=(self.pk, ))
models.Model.get_admin_change_url = get_admin_change_url

def get_admin_delete_url(self):
    return reverse(self._admin_url_name('delete'), args=(self.pk, ))
models.Model.get_admin_delete_url = get_admin_delete_url

def get_admin_history_url(self):
    return reverse(self._admin_url_name('history'), args=(self.pk, ))
models.Model.get_admin_history_url = get_admin_history_url

def get_admin_changelist_url(self):
    return reverse(self._admin_url_name('changelist'))
models.Model.get_admin_changelist_url = get_admin_changelist_url

def get_admin_add_url(self):
    return reverse(self._admin_url_name('add'))
models.Model.get_admin_add_url = get_admin_add_url

models.Model.get_verbose_name = lambda self: self._meta.verbose_name
models.Model.get_verbose_name_plural = lambda self: self._meta.verbose_name_plural

version = ('0', '0', '2', 'alpha')

