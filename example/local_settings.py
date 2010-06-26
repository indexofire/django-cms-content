# -*- coding: utf-8 -*-

gettext = lambda s: s

# django-cms-2.0 Settings:
APPEND_SLASH = True
CMS_SOFTROOT = True
CMS_MODERATOR = False
CMS_PERMISSION = True
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_FLAT_URLS = False
CMS_MENU_TITLE_OVERWRITE = True
CMS_HIDE_UNTRANSLATED = False
CMS_URL_OVERWRITE = True
LANGUAGES = (
    ('en-us', gettext('English')),
    ('zh-cn', gettext("Chinese")),
)
CMS_TEMPLATES = (
    ('base.html', gettext('default')),
    ('col_two.html', gettext('two columns')),
    ('col_three.html', gettext('three columns')),
    ('nav_playground.html', gettext('navigation examples')),
)
CMS_PLACEHOLDER_CONF = {
    'col_sidebar': {
        'plugins': (
            'TextPlugin',
            'LinkPlugin',
        ),
        'name': gettext("sidebar column"),
    },
    'col_left': {
        'plugins': (
            'TextPlugin',
            'GoogleMapPlugin',
            'ReSTPlugin',
            'PicturePlugin',
            'LinkPlugin',
        ),
        'name': gettext("left column"),
    },
    'col_right': {
        'plugins': (
            'LinkPlugin',
            'PicturePlugin',
            'TextPlugin',
            'GoogleMapPlugin',
            'ReSTPlugin', 
        ),
        'name': gettext("right column"),
    },
}

# south
SOUTH_TESTS_MIGRATE = False

# cms_content
CMS_CONTENT_EDITOR = 'WYMEditor'
CMS_CONTENT_ROOT_URL = '/cms/'
CMS_CONTENT_CODE_HIGHLIGHT = True
CMS_CONTENT_CODE_HIGHLIGHT_CSS = 'code_highlight'
CMS_CONTENT_CODE_HIGHLIGHT_LINENOS = True
