#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'dotmobo'
SITENAME = "DotMobo"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = None

# Social widget
SOCIAL = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Theme
THEME = "alchemy"
SITE_SUBTEXT = "Blog d'un Pythoniste Djangonaute"
PROFILE_IMAGE = "https://pbs.twimg.com/profile_images/559712938420760577/Hraa9PBv_200x200.jpeg"
GITHUB_ADDRESS = "https://github.com/dotmobo"
TWITTER_ADDRESS = "https://twitter.com/dotmobo"
EXTRA_FAVICON = False
LICENSE_NAME = "MIT"
LICENSE_URL = "https://opensource.org/licenses/MIT"
MENU_ITEMS = {}
META_DESCRIPTION = "DotMobo - Blog d'un Pythoniste Djangonaute"
PAGES_ON_MENU = True
CATEGORIES_ON_MENU = True
TAGS_ON_MENU = True
ARCHIVES_ON_MENU = True
SHOW_ARTICLE_AUTHOR = False
GOOGLEPLUS_ADDRESS = "https://www.google.com/+DotmoboGithubIo6"

# Plugins
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
