# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from cms.models.fields import PlaceholderField
import datetime

class CMSSection(models.Model):
    """
    models for CMS's Sections
    """
    name = models.CharField(_(u"Section Name"), max_length=20)
    slug = models.CharField(_(u"Slug"), max_length=100)
    sort = models.IntegerField(_(u"Sort"), default=1)
    description = models.TextField(_(u"Section Description"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Section List')
        verbose_name_plural = _(u'Section List')

    def get_absolute_url(self):
        #return reverse('section_view', args=[self.pk])
        pass

class CMSCategory(models.Model):
    """
    models for CMS's Categories
    """
    name = models.CharField(_(u"Category Name"), max_length=20)
    parent = models.ForeignKey(CMSSection, verbose_name=_(u"Section"), blank=True, null=True)
    description = models.TextField(_(u"Category Description"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Category List')
        verbose_name_plural = _(u'Category List')

    def get_absolute_url(self):
        return reverse('category_view', args=[self.pk])


class CMSArticle(models.Model):
    """
    models for CMS's Articles
    """
    title = models.CharField(_(u"Article Title"), max_length=100)
    content = models.TextField(_(u"Article Content"))
    user = models.ForeignKey(User, verbose_name=_(u"Author Name"))
    created = models.DateTimeField(_(u"Created Date"), auto_now_add=True)
    modified = models.DateTimeField(_(u"Last Modified Date"))
    category = models.ForeignKey(CMSCategory, verbose_name=_(u"Category"))

    class Meta:
        ordering = ['-created']
        verbose_name = _(u'Article List')
        verbose_name_plural = _(u'Article List')
        get_latest_by = 'created'

    def __unicode__(self):
        return u'%s - %s' % (self.user.username, self.title)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        super(CMSArticle, self).save(*args, **kwargs)
        if not CMSArticle.objects.filter(category__pk__exact=self.category.pk).count():
            self.category.delete()
            return None
        self.category.latest_post = self
        self.category.save()

    def get_absolute_url(self):
        return reverse('article_view', args=[self.pk])

