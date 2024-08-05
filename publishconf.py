#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://dotmobo.xyz'
RELATIVE_URLS = False

FEED_ATOM = 'feeds/all.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#Disqus
DISQUS_SITENAME = "dotmobo"

GOOGLE_ANALYTICS = "UA-68852219-1"


GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-1630762128981156',
    'page_level_ads': False,          # Allow Page Level Ads (mobile)
    'ads': {
        'aside': '6859931822',          # Side bar banner (all pages)
        'main_menu': '',      # Banner before main menu (all pages)
        'index_top': '',      # Banner after main menu (index only)
        'index_bottom': '',   # Banner before footer (index only)
        'article_top': '',    # Banner after article title (article only)
        'article_bottom': '', # Banner after article content (article only)
    }
}