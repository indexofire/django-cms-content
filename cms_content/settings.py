# -*- coding: utf-8 -*-
from django.conf import settings

# config the root URL path of cms_content page
# if your cms_content page's url is http://yourdomain.com/cms/content/, then
# define the value to CMS_CONTENT_ROOT_URL in your project's settings.py
ROOT_URL = getattr(settings, 'CMS_CONTENT_ROOT_URL', '/cms/')

# config code highlight templatetags
CODE_HIGHLIGHT = getattr(settings, 'CMS_CONTENT_CODE_HIGHLIGHT', True)
CODE_HIGHLIGHT_CSS = getattr(settings, 'CMS_CONTENT_CODE_HIGHLIGHT_CSS', 'code_highlight')
CODE_HIGHLIGHT_LINENOS = getattr(settings, 'CMS_CONTENT_CODE_HIGHLIGHT_LINENOS', False)
CODE_HIGHLIGHT_DEFAULT = getattr(settings, 'CMS_CONTENT_CODE_HIGHLIGHT_DEFAULT', 'text')

# config Article's Editor in admin
# right now there are two choice: `WYMEditor` or `TinyMCE`
# if you want to use TinyMCE as your editor, put CMS_CONTENT_EDITOR = 'TinyMCE'
# in your project's settings.py
EDITOR = getattr(settings, 'CMS_CONTENT_EDITOR', 'WYMEditor')

# paginator
ARTICLE_PERPAGE = getattr(settings, 'CMS_CONTENT_ARTICLE_PERPAGE', 10)

# comment spam setting
AKISMET_API_KEY = '773ea92115d8'

# image upload_to
UPLOAD_TO = getattr(settings, 'CMS_CONTENT_UPLOAD_TO', 'upload')

# tag settings
# define the minimal weight of a tag in the tagcloud
TAGCLOUD_MIN = getattr(settings, 'TAGGIT_TAGCLOUD_MIN', 1.0)
# define the maximum weight of a tag in the tagcloud 
TAGCLOUD_MAX = getattr(settings, 'TAGGIT_TAGCLOUD_MAX', 6.0) 
