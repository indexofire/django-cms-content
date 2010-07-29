# -*- coding: utf-8 -*-
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('administrator', 'administrator@localhost.com'),
)
MANAGERS = ADMINS

DATABASE_FILE = os.path.join(PROJECT_PATH, 'database/data.sql')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_FILE,
        'OPTIONS': {
            'timeout': 10,
        }
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Change to you own KEY
SECRET_KEY = 'f89543m_$!8095423mgfa841$!_+63256349-9-*$!*)#@!_49'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'cms.context_processors.media',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'cms',
    'mptt',
    'publisher',
    'menus',
    'cms.plugins.text',
    'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.picture',
    #'south',
    'reversion',
    'dbgettext',
    'cms_content',
)

try:
    from settings_local import *
except ImportError:
    pass

