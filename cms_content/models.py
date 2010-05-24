# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from cms.models.fields import PlaceholderField

class CMSSection(models.Model):
    """Models For Django CMS Sections:
    Create a section to contain all category belong to it.
    """
    name = models.CharField(_(u"Section Name"), max_length=20)
    slug = models.CharField(_(u"Slug"), max_length=100)
    description = models.TextField(_(u"Section Description"))
    created = models.DateTimeField(_(u"Created Date"), auto_now_add=True)
    modified = models.DateTimeField(_(u"Last Modified Date"), auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Section')

    def get_absolute_url(self):
        #return reverse('section_id', args=[self.pk])
        return "%s/" % self.slug

class CMSCategory(models.Model):
    """Models for CMS's Categories:
    Create a category which is belong to a section.
    """
    name = models.CharField(_(u"Category Name"), max_length=40)
    slug = models.CharField(_(u"Slug"), max_length=100)
    section = models.ForeignKey(CMSSection, verbose_name=_(u"Section"), blank=True, null=True)
    description = models.TextField(_(u"Category Description"))
    created = models.DateTimeField(_(u"Created Date"), auto_now_add=True)
    modified = models.DateTimeField(_(u"Last Modified Date"), auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Category')

    def get_absolute_url(self):
        #return reverse('category_view', args=[self.pk])
        return "%s/" % self.slug


class CMSArticle(models.Model):
    """Models for CMS's Articles:
    one article in one category.
    """
    title = models.CharField(_(u"Article Title"), max_length=100)
    slug = models.CharField(_(u"Slug"), max_length=100)
    content = models.TextField(_(u"Article Content"))
    created_by = models.ForeignKey(User, verbose_name=_(u"Author Name"), related_name="author")
    created_date = models.DateTimeField(_(u"Created Date"), auto_now_add=True)
    last_modified_by = models.ForeignKey(User, verbose_name=_(u"Last Modified By"), related_name="revisor")
    last_modified_date = models.DateTimeField(_(u"Last Modified Date"), auto_now=True)
    category = models.ForeignKey(CMSCategory, verbose_name=_(u"Category"))
    is_published = models.BooleanField(_(u"Publish It"))

    class Meta:
        ordering = ['-created_by']
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __unicode__(self):
        return u'%s - %s' % (self.created_by.username, self.title)

    #def save(self, *args, **kwargs):
    #    self.modified = datetime.datetime.now()
    #    super(CMSArticle, self).save(*args, **kwargs)
    #    if not CMSArticle.objects.filter(category__pk__exact=self.category.pk).count():
    #        self.category.delete()
    #        return None
    #    self.category.latest_post = self
    #    self.category.save()

    def get_absolute_url(self):
        #return reverse('article_view', args=[self.pk])
        return "%s/" % self.id

