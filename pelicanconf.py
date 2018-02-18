#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHORS = {
    'Onur Aslan': {
        'description': """
            I am a superhero saving thousand of lives in Internet.
        """,
        'cover': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Milky_Way_Arch.jpg/1920px-Milky_Way_Arch.jpg',
        'image': 'https://lh6.googleusercontent.com/-zEMaXmWAhdI/AAAAAAAAAAI/AAAAAAAAAAA/eVdgsm3TIDU/s128-c-k/photo.jpg',
        'links': (('github', 'https://github.com/onuraslan'),
                  ('twitter-square', 'https://twitter.com/oasln')),
    },

    'Gilles Vandewiele': {
        'description': """
            White-box machine learning and decision support systems.
        """,
        'cover': '/images/banner_gilles.jpg',
        'image': '/images/profielfoto_gilles.jpg',
        'links': (('github', 'https://github.com/GillesVandewiele'),
                  ('twitter-square', 'https://twitter.com/gillesvdwiele'),
                  ('linkedin', 'https://www.linkedin.com/in/gillesvandewiele')),
    },

    'Pieter Bonte': {
        'description': """
            Stream reasoning.
        """,
        'cover': '/images/banner_gilles.jpg',
        'image': '/images/profielfoto_pieter.jpg',
        'links': (('github', 'https://github.com/pbonte/'),
                  ('twitter-square', 'https://twitter.com/psbonte'),
                  ('linkedin', ' https://www.linkedin.com/in/pieter-bonte-9294315a')),
    }
}
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
    ('About', '/about.html'),
    ('Publications', '/publications.html'),
    ('Blog', '/blog.html'),
    )

# Blogroll
LINKS = (('IDLab', 'http://idlab.technology'),
         ('UGent', 'http://www.ugent.be/'))

ICONS = (
    ('github', 'https://github.com/IBCNServices'),
)

DIRECT_TEMPLATES = ('includes/posts', 'publications', 'index', 'about', 'blog')
PAGINATED_DIRECT_TEMPLATES = ('index', 'includes/posts', 'publications', 'blog') 

PUBLICATIONS_SRC = 'content/publications.bib'

MEDIUS_AUTHORS = AUTHORS

SITESUBTITLE = 'Exploiting domain knowledge to enable more intelligent machine learning, event processing and personalized & context-aware decision support systems'

DEFAULT_PAGINATION = 5
