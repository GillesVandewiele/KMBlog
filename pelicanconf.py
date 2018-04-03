#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Add the path where this file is in to the SYSPATH
# else, the import will fail (this file is used in
# the pelican framework)
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path)

from rdfparser import extract_authors


AUTHORS_PATH = 'content/authors'       
AUTHORS = extract_authors(AUTHORS_PATH)

SITENAME = 'Knowledge Management'
SITEURL = ''
THEME = 'medius'

PATH = 'content'

TIMEZONE = 'Europe/Brussels'

DESCRIPTION = 'Exploiting background/domain knowledge to enable more intelligent machine learning, event processing and personalized & context-aware decision support systems'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['pelican-bibtex']

STATIC_PATHS = ['images']


MENUITEMS = (
    ('About', SITEURL+'/about.html'),
    ('Publications', SITEURL+'/publications.html'),
    ('Blog', SITEURL+'/blog.html'),
    #('Conferences', SITEURL+'/conferences.html'),
    )

# Blogroll
LINKS = (('IDLab', 'http://idlab.technology'),
         ('UGent', 'http://www.ugent.be/'))

ICONS = (
    ('github', 'https://github.com/IBCNServices'),
)

DIRECT_TEMPLATES = ('includes/posts', 'publications', 'index', 'about', 'blog', 'conferences')
PAGINATED_DIRECT_TEMPLATES = ('index', 'includes/posts', 'publications', 'blog') 
DISQUS_SITENAME = "localhost"

PUBLICATIONS_SRC = 'content/publications'

MEDIUS_AUTHORS = AUTHORS

SITESUBTITLE = 'Exploiting domain knowledge to enable more intelligent machine learning, event processing and personalized & context-aware decision support systems'

DEFAULT_PAGINATION = 5
