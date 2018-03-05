import logging
logger = logging.getLogger(__name__)

from pelican.generators import Generator, CachingGenerator
from pelican.readers import BaseReader
from pelican.utils import *
from pelican import signals

import os
import re

from pybtex.database.input.bibtex import Parser
from pybtex.database.output.bibtex import Writer
from pybtex.database import BibliographyData, PybtexError
from pybtex.backends import html
from pybtex.style.formatting import plain

from collections import defaultdict

import latexcodec
from pylatexenc.latex2text import LatexNodes2Text

BIBTEX_TYPE_TO_TEXT = {
    'inproceedings': 'Conference',
    'article': 'Journal',
    'book': 'Book',
    'booklet': 'Book',
    'conference': 'Conference',
    'proceedings': 'Conference',
    'phdthesis': 'Thesis',
    'mastersthesis': 'Thesis',
    'unpublished': 'Unpublished',
    'misc': 'Unpublished',
    'techreport': 'Technical Report',
}

class Publication(object):
    def __init__(self, key, authors, title, year, where, 
                 abstract=None, pdf_url=None, resource_urls=None):
        """A publication object, has the following fields:

            * key (str): unique identifier
            * authors (list (str))
            * title (str)
            * year (int)
            * where (str)
            * information (str)
            * abstract (str)
            * pdf_url (str)
            * resource_urls (list(tuple(str)) ('name', 'url'))
        """
        self.key = key
        self.authors = authors
        self.title = title
        self.year = year
        self.where = where
        self.abstract = abstract
        self.pdf_url = pdf_url
        self.resource_urls = resource_urls
        self.citations = {
            'bib': 'test1',
            'IEEE': 'test2',
            'ACM': 'test3',
            'LNCS': 'test4',
            'APA': 'test5',
            'MLA': 'test6'
        }


    def create_citation_formats(self):
        # TODO: use the different variables of an object
        # to create different citation formats
        pass

class BibGenerator(Generator):
    enabled = True

    def __init__(self, *args, **kwargs):
        self.publications = []
        self.publications_per_year = defaultdict(list)
        self.publications_per_type = defaultdict(list)
        self.publications_per_author = defaultdict(list)
        self.publications_per_type_rev = defaultdict(set)
        super(BibGenerator, self).__init__(*args, **kwargs)
        signals.generator_init.send(self)

    def add_publications(self):
        # Check if PUBLICATIONS_SRC is set
        if 'PUBLICATIONS_SRC' not in self.settings:
            logger.warn('PUBLICATIONS_SRC not set')
            return

        # Try to parse the bibtex files
        pub_dir = self.settings['PUBLICATIONS_SRC']
        try:
            bibdata_all = BibliographyData()
            for file in os.listdir(pub_dir):
                with codecs.open(pub_dir+os.sep+file, 'r', encoding="utf8") as stream:
                    bibdata = Parser().parse_stream(stream)
                    key, entry = bibdata.entries.items()[0]
                    bibdata_all.entries[key] = entry
        except PybtexError as e:
            logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
                refs_file,
                str(e)
            ))
            return

        # Create Publication objects and add them to a list
        publications = []

        # format entries
        plain_style = plain.Style()
        formatted_entries = list(plain_style.format_entries(bibdata_all.entries.values()))

        decoder = latexcodec.lexer.LatexIncrementalDecoder()

        for entry in bibdata_all.entries:
            raw_tex = BibliographyData(entries={entry: bibdata_all.entries[entry]}).to_string('bibtex')
            #raw_tex += '\n}'
            formatted_entry = list(plain_style.format_entries([bibdata_all.entries[entry]]))[0]

            key = formatted_entry.key
            entry = bibdata_all.entries[key]

            year = entry.fields.get('year', 2018)
            
            authors = entry.fields.get('author', '').split(' and ')
            authors = [
                LatexNodes2Text().latex_to_text(
                    re.sub(r'[\{\}]', '', (x.split(',')[1] + ' ' + x.split(',')[0]).strip())
                )
                for x in authors
            ]
            
            title = LatexNodes2Text().latex_to_text(entry.fields.get('title', ''))
            
            pdf = entry.fields.get('pdf', None)
            slides = entry.fields.get('slides', None)
            poster = entry.fields.get('poster', None)

            where = ''
            if 'booktitle' in entry.fields:
                where = LatexNodes2Text().latex_to_text(entry.fields.get('booktitle'))
            elif 'journal' in entry.fields:
                where = LatexNodes2Text().latex_to_text(entry.fields.get('journal'))
            
            abstract = entry.fields.get('abstract', '')

            pub = Publication(
                key, authors, title, 
                year, where,
                abstract=abstract,
                pdf_url=pdf, 
                resource_urls=[
                    ('slides', slides),
                    ('poster', poster)
                ]
            )
            pub.citations['bib'] = raw_tex.rstrip('\r\n')
            publications.append(pub)
            self.publications_per_year[pub.year].append(pub)
            for author in authors:
                if author in self.context['MEDIUS_AUTHORS'].keys():
                    self.publications_per_author[author].append(pub)
            self.publications_per_type[BIBTEX_TYPE_TO_TEXT[entry.type]].append(pub)
            self.publications_per_type_rev[pub] = BIBTEX_TYPE_TO_TEXT[entry.type]


        return publications

    def generate_context(self):
        publications = self.add_publications()
        self.context['publications'] = publications
        self.publications = publications
        self.context['publications_per_year'] = self.publications_per_year
        self.context['publications_per_type'] = self.publications_per_type
        self.context['publications_per_author'] = self.publications_per_author
        self.context['publications_per_type_rev'] = self.publications_per_type_rev

    def generate_publications(self, write):
        publication_template = self.get_template('publication')
        for publication in self.publications:
            pub_context = self.context.copy()
            pub_context['publication'] = publication
            write('publications/{}.html'.format(publication.key), publication_template, pub_context)

    def generate_output(self, writer):
        x = self.settings['PUBLICATIONS_SRC']
        write = partial(writer.write_file,
                        relative_urls=self.settings['RELATIVE_URLS'])
        self.generate_publications(write)

def get_bib_generator(generator):
    # define a new generator here if you need to
    settings = generator.settings
    return BibGenerator

def register():
    signals.get_generators.connect(get_bib_generator)