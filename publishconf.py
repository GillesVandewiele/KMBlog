#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITENAME = 'Knowledge Management'
SITEURL = 'https://gillesvandewiele.github.io/KMBlog'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = False

MENUITEMS = (
    ('About', SITEURL+'/about.html'),
    ('Publications', SITEURL+'/publications.html'),
    ('Blog', SITEURL+'/blog.html'),
    ('Conferences', SITEURL+'/conferences.html'),
    )


AUTHORS = extract_authors(AUTHORS_PATH, SITEURL)
MEDIUS_AUTHORS = AUTHORS



# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
