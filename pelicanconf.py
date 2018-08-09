#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'dotmobo'
SITEURL = ''
SITENAME = ".mobo"
SITETITLE = SITENAME
SITESUBTITLE = "Blog d'un Pythoniste Djangonaute"
SITEDESCRIPTION = "DotMobo - Blog d'un Pythoniste Djangonaute"
SITELOGO = "//pbs.twimg.com/profile_images/559712938420760577/Hraa9PBv_200x200.jpeg"
FAVICON = None
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'

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
          ('google', "https://www.google.com/+DotmoboGithubIo6"),
          ('rss', '//dotmobo.github.io/feeds/all.atom.xml'))


MENUITEMS = (('Categories', '/categories.html'),
             ('Tags', '/tags.html'),
             ('Archives', '/archives.html'))


CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}



COPYRIGHT_YEAR = 2018

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
STATIC_PATHS = ['images']

USE_LESS = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True