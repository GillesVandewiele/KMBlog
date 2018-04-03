#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import rdflib
import os



def extract_authors(author_path, site_url=''):
    g = rdflib.Graph()
    for author_rdf_file in os.listdir(author_path):
        g.parse(AUTHORS_PATH+os.sep+author_rdf_file, format='turtle')

    # Get all unique author URIs
    qres = g.query("""SELECT ?author  WHERE {
                        ?author rdf:type foaf:Person .
                   }""",
                   initNs={'rdf': rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
                           'foaf': rdflib.Namespace('http://xmlns.com/foaf/0.1/')})
    authors = [x[0] for x in qres]

    author_dict = {}
    for author in authors:
        # Get the name
        qres = g.query("""SELECT ?name  WHERE {
                        ?author foaf:name ?name .
                   }""",
                   initNs={'foaf': rdflib.Namespace('http://xmlns.com/foaf/0.1/')},
                   initBindings={'author': author})
        name = str(list(qres)[0][0].toPython())
        author_dict[name] = {}

        # Get his interests
        qres = g.query("""SELECT ?interest  WHERE {
                        ?author foaf:interest ?interest .
                   }""",
                   initNs={'foaf': rdflib.Namespace('http://xmlns.com/foaf/0.1/')},
                   initBindings={'author': author})
        # Build the description string based on his interests
        if len(qres) == 1:
            description = str(list(qres)[0][0].toPython())
        else:
            interests = [str(x[0].toPython()) for x in qres]
            description = ','.join(interests[:-2]) + ' and '.join(interests[-2:])
        author_dict[name]['description'] = description

        # Get his image
        qres = g.query("""SELECT ?image  WHERE {
                        ?author foaf:depiction ?image .
                   }""",
                   initNs={'foaf': rdflib.Namespace('http://xmlns.com/foaf/0.1/')},
                   initBindings={'author': author})
        image = list(qres)[0][0]
        if type(image) == rdflib.term.Literal:
            image = site_url+'/images/'+str(image.toPython())
        else:
            image = str(image.toPython())

        # Set the image and cover image
        author_dict[name]['image'] = image
        author_dict[name]['cover'] = site_url+'/images/banner.png'

        # Get the links
        author_dict[name]['links'] = []
        qres = g.query("""SELECT ?account  WHERE {
                        ?author foaf:account ?account .
                   }""",
                   initNs={'foaf': rdflib.Namespace('http://xmlns.com/foaf/0.1/')},
                   initBindings={'author': author})

        for link in qres:
            uri = str(link[0].toPython())
            if 'github' in uri:
                author_dict[name]['links'].append(('github', uri))
            elif 'twitter' in uri:
                author_dict[name]['links'].append(('twitter-square', uri))
            elif 'linkedin' in uri:
                author_dict[name]['links'].append(('linkedin', uri))
            else:
                author_dict[name]['links'].append(('globe', uri))

        author_dict[name]['links'] = sorted(author_dict[name]['links'], key=lambda x: x[0])

    return author_dict



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
