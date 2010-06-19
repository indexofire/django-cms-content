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

Adding a page in admin and giving a name of it, for example 'content', and it 
has a root page whose name is 'cms'. so the url for the cms will be /cms/content/
as default. revise the value of CMS_CONTENT_URL to it in cms_content/settings.py

Now, open your browser visit the content.
