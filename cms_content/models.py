# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.signals import comment_was_posted
from django.utils.translation import ugettext_lazy as _

from cms_content.settings import ROOT_URL
from cms_content.settings import UPLOAD_TO


__all__ = [
    'CMSMenuID',
    'CMSSection',
    'CMSCategory',
    'CMSArticle',
]

class CMSMenuID(models.Model):
    """All CMS_Content object's menu id for django-cms get_nodes"""
    menuid = models.IntegerField(blank=False,null=False)
    parent = models.IntegerField(blank=True,null=True)
    
    class Meta:
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
    slug = models.SlugField(
        _(u"Slug"),
        max_length=255,
        blank=False,
        unique=True,
        help_text=_(u"Section's Slug"),
    )
    description = models.TextField(
        _(u"Section Description"),
        blank=False,
    )
    image = models.ImageField(
        _(u"Image"),
        upload_to=UPLOAD_TO,
        blank=True,
        help_text=_(u"Section Image Display in Pages"),
    )
    created_date = models.DateTimeField(
        _(u"Create Time"),
        auto_now_add=True,
    )
    menu = models.OneToOneField(CMSMenuID)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_date']
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Section')

    @property
    def url(self):
        return "%s%s/%s/" % (ROOT_URL, 'section', self.slug)
    
    @models.permalink
    def get_absolute_url(self):
        return ('cms_content_section_detail', (self.slug,))


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
    slug = models.SlugField(
        _(u"Slug"),
        max_length=255,
        blank=False,
        unique=True,
        help_text=_(u"Category's Slug"),
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
    image = models.ImageField(
        _(u"Image"),
        upload_to=UPLOAD_TO,
        blank=True,
        help_text=_(u"Category Image Display in Pages"),
    )
    created_date = models.DateTimeField(
        _(u"Create Time"),
        auto_now_add=True,
    )
    menu = models.OneToOneField(CMSMenuID)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_date']
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Category')

    @property
    def url(self):
        return "%s%s/%s/" % (ROOT_URL, 'category', self.slug)
    
    @models.permalink
    def get_absolute_url(self):
        return ("cms_content_category_detail", (self.slug,))


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
    slug = models.SlugField(
        _(u"Slug"),
        max_length=255,
        blank=False,
        unique=True,
        help_text=_(u"Article's Slug"),
    )
    content = models.TextField(
        _(u"Article Content"),
        blank=False,
        help_text=_(u"Article's Content"),
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

    @property
    def previous_article(self):
        """Return the previous article"""
        articles = CMSArticle.objects.filter(created_date_lt=self.created_date)
        if articles:
            return articles[0]
    
    @property
    def next_article(self):
        """Return the next article"""
        articles = CMSArticle.objects.filter(created_date_gt=self.created_date)
        if articles:
            return articles[0]
    
    @property
    def url(self):
        return ROOT_URL + 'article/' + "%s/%s/%s/%s/" % (
            self.created_date.strftime('%Y'),
            self.created_date.strftime('%m'),
            self.created_date.strftime('%d'),
            self.slug,
            )

    @models.permalink
    def get_absolute_url(self):
        return ('cms_content_article_detail', None, {
            "year":  self.created_date.strftime('%Y'),
            "month": self.created_date.strftime('%m'),
            "day":   self.created_date.strftime('%d'),
            "slug":  self.slug,
            }
        )

def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    """Spam checking can be enabled/disabled per the comment's target Model

    Usage:
    if comment.content_type.model_class() != CMSArticle:
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
