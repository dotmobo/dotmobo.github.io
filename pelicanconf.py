#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'dotmobo'
SITEURL = 'http://127.0.0.1:8000'
SITENAME = ".mobo"
SITETITLE = SITENAME
SITESUBTITLE = "Explorations d'un développeur"
SITEDESCRIPTION = ".mobo - explorations d'un développeur"
SITELOGO = "//dotmobo.xyz/images/avatar700.jpg"
FAVICON = None
BROWSER_COLOR = '#333333'

THEME_COLOR = 'dark'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

PYGMENTS_STYLE = 'emacs'
PYGMENTS_STYLE_DARK = 'monokai'

ROBOTS = 'index, follow'

THEME = "../pelican-themes/Flex"
PATH = 'content'
TIMEZONE = 'Europe/Paris'

# Default theme language.
I18N_TEMPLATES_LANG = 'en'
# Your language.
DEFAULT_LANG = 'fr'
OG_LOCALE = 'fr_FR'

DATE_FORMATS = {
    'fr': '%d/%m/%Y',
}

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
HOME_HIDE_TAGS = True

LINKS = None


SOCIAL = (('github', 'https://github.com/dotmobo'),
          ('twitter', 'https://twitter.com/dotmobo'),
          ('rss', '//dotmobo.xyz/feeds/all.atom.xml'))


MENUITEMS = (('Categories', '/categories.html'),
             ('Tags', '/tags.html'),
             ('Archives', '/archives.html'))


CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}



COPYRIGHT_YEAR = 2024

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['sitemap', 'i18n_subsites']

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

# static
STATIC_PATHS = ['images', 'css', "extra/CNAME"]

EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'css/custom.css'},
    "extra/CNAME": {"path": "CNAME"},
}


CUSTOM_CSS = 'css/custom.css'

USE_LESS = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True