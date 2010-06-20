============================
Django CMS 2.0 Content App
============================

.. contents::

1. Introduction
----------------------------

`Django CMS 2.0`_ is a django app to build your content management site. It uses
mptt_ to manage different pages which load your content. However, I think there
is some problems if you have a lot of pages.

1. It's hard to manage these complicated relationship of these pages.
2. Without pagination as default setting, the admin interface will be slow down
by your page list and confused to what content at where.

Well, luckily django-cms-2.0 has the ability to extend or integrate other app
into it. So I create this app to build a simple three levels relationship which
comes from joomla_ , a PHP CMS program.

.. _`Django CMS 2.0`: http://www.django-cms.org
.. _mptt: http://code.google.com/p/django-mptt/
.. _joomla: http://www.joomla.org

2. Usage
-----------------------------

2.1 Install
*****************************

Install the app is simple like any other django app, you just need to insert
`cms_content` into your INSTALLED_APP of your project settings file like this:

::

   INSTALLED_APPS = (
       ...
       'cms_content',
       ...
   )

copy or link media/cms_content folder to your media folder.

Adding a page in admin and giving a name of it, for example 'content'. set 
*attached menu* to CMS Content Menu and *application* to CMS Section in the
page's advanced settings. And if the content page has a root page whose name is 
'cms', then the url for the cms will be /cms/content/ as default. revise the 
value of CMS_CONTENT_URL to it in cms_content/settings.py

::

   CMS_CONTENT_URL = '/cms/content/'

in admin, create your sections and categories, then add articles. After that 
open your browser, visit /cms/content/ URL, you will see the all your articles.

2.2 Setup
*****************************

The default WYSIWYG editor is WYMEditor. You can use TinyMCE via changing widget
in forms.py.

If your site is nothing about programing or you don't want to use code highlight,
please remove templatetag *pygmentize* and *pygments.css* file in 
template/cms_content/article.html

2.3 Dependencies
*****************************

Because default WYSIWYG editor 'WYMEditor' was supported pygments code highlight,
so django-cms-2.0-content has dependencies:

* BeautifulSoup_
* Pygments_

.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
.. _Pygments: http://pygments.org/
