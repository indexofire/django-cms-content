# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.signals import comment_was_posted
from django.utils.translation import ugettext_lazy as _


__all__ = ['CMSSection', 'CMSCategory', 'CMSArticle']

class CMSMenuID(models.Model):
    """All CMS_Content entries' menu id"""
    menuid = models.IntegerField(blank=False)
    parent = models.IntegerField(blank=True)
    
    class Meta:
        #ordering = ['-menu']
        verbose_name = _(u'Menu ID')
        verbose_name_plural = _(u'Menu ID')

class CMSSection(models.Model):
    """Models For Django CMS Sections:

    Section is the first level of cms_content structure which contains category.
    Create a section first before to build your categories belong.
    """

    name = models.CharField(
        _(u"Section Name"),
        max_length=255,
        blank=False,
    )
    slug = models.CharField(
        _(u"Slug"),
        max_length=255,
        blank=False,
    )
    description = models.TextField(
        _(u"Section Description"),
        blank=False,
    )
    created_date = models.DateTimeField(
        _(u"Created Date"),
        auto_now_add=True,
    )
    menu = models.OneToOneField(CMSMenuID)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_date']
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Section')

    @models.permalink
    def get_absolute_url(self):
        return reverse('section_detail', (self.slug,))


class CMSCategory(models.Model):
    """Models for CMS's Categories:

    Category is the second level of cms_content structure. Before publish any
    article, create a category to which is belong a section.
    """

    name = models.CharField(
        _(u"Category Name"),
        max_length=255,
        blank=False,
    )
    slug = models.CharField(
        _(u"Slug"),
        max_length=255,
        blank=False,
    )
    section = models.ForeignKey(
        CMSSection,
        verbose_name=_(u"Section"),
        related_name="category_of_section",
        blank=False,
    )
    description = models.TextField(
        _(u"Category Description"),
        blank=False,
    )
    created_date = models.DateTimeField(
        _(u"Created Date"),
        auto_now_add=True,
    )
    menu = models.OneToOneField(CMSMenuID)

    class Meta:
        ordering = ['-created_date']
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Category')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        #mode = getattr(settings, "LIST_MODE", "table")
        #return reverse('category_%s' % mode, args=[self.slug])
        return ("category_detail", None, {
            "slug": self.slug,
            },
        )


class CMSArticle(models.Model):
    """Models for CMS's Articles:

    Article is the third level of cms_content structure. Every article contains
    the content you write.
    """

    PUB_STATUS = (
        (_(u'pub'), u'published'),
        (_(u'del'), u'deleted'),
        (_(u'dra'), u'draft'),
    )

    title = models.CharField(
        _(u"Article Title"),
        max_length=255,
        blank=False,
    )
    slug = models.CharField(
        _(u"Slug"),
        max_length=255,
        blank=False,
    )
    content = models.TextField(
        _(u"Article Content"),
        blank=False,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_(u"Author Name"),
        related_name="cms_article_author",
        blank=False,
    )
    created_date = models.DateTimeField(
        _(u"Created Date"),
        auto_now_add=True,
    )
    last_modified_by = models.ForeignKey(
        User,
        verbose_name=_(u"Last Modified By"),
        related_name="cms_article_revisor",
    )
    last_modified_date = models.DateTimeField(
        _(u"Last Modified Date"),
        auto_now=False,
    )
    category = models.ForeignKey(
        CMSCategory,
        verbose_name=_(u"Category"),
        related_name="article_of_category",
    )
    pub_status = models.CharField(
        _(u"Article Publish Status"),
        max_length=3,
        choices=PUB_STATUS,
    )
    hits = models.IntegerField(
        _(u"Article His Number"),
        default=1,
    )
    pub_start_date = models.DateTimeField(
        _(u"Article Publish Start Date"),
        blank=True,
        null=True,
    )
    pub_end_date = models.DateTimeField(
        _(u"Article Publish End Date"),
        blank=True,
        null=True,
    )
    menu = models.OneToOneField(CMSMenuID)
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __unicode__(self):
        return u'%s - %s' % (self.created_by.username, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ("article_detail", (), {
            "year": self.created_date.strftime('%Y'),
            "month": self.created_date.strftime('%m'),
            "day": self.created_date.strftime('%d'),
            "slug": self.slug,
            }
        )


def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    """Spam checking can be enabled/disabled per the comment's target Model

    Usage:
    if comment.content_type.model_class() != Entry:
        return
    """

    try:
        from akismet import Akismet
    except:
        return

    ak = Akismet(
        key=settings.AKISMET_API_KEY,
        blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )
    if ak.verify_key():
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': 'comment',
            'comment_author': comment.user_name.encode('utf-8'),
        }

    if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
        comment.flags.create(
            user=comment.content_object.author,
            flag='spam'
        )
        comment.is_public = False
        comment.save()
comment_was_posted.connect(on_comment_was_posted)
