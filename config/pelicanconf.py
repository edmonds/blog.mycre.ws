#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Robert Edmonds'
EMAIL = u'edmonds@mycre.ws'
SITENAME = u"Robert Edmonds' blog"
SITEURL = 'http://blog.mycre.ws'

DEFAULT_LANG = u'en'
TIMEZONE = 'UTC'

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None

RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = False

ARTICLE_URL = 'articles/{slug}/'
ARTICLE_SAVE_AS = 'articles/{slug}/index.html'

AUTHOR_SAVE_AS = False
CATEGORY_SAVE_AS = False

DIRECT_TEMPLATES = ('index',)

THEME = './theme'

MD_EXTENSIONS = ('extra',)
