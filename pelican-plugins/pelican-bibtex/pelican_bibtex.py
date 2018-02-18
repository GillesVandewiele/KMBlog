"""
Pelican BibTeX
==============

A Pelican plugin that populates the context with a list of formatted
citations, loaded from a BibTeX file at a configurable path.

The use case for now is to generate a ``Publications'' page for academic
websites.
"""
# Author: Vlad Niculae <vlad@vene.ro>
# Unlicense (see UNLICENSE for details)

import logging
logger = logging.getLogger(__name__)

from pelican import signals

__version__ = '0.2.1'


def add_publications(generator):
    """
    Populates context with a list of BibTeX publications.

    Configuration
    -------------
    generator.settings['PUBLICATIONS_SRC']:
        local path to the BibTeX file to read.

    Output
    ------
    generator.context['publications']:
        List of tuples (key, year, text, bibtex, pdf, slides, poster).
        See Readme.md for more details.
    """
    if 'PUBLICATIONS_SRC' not in generator.settings:
        return
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    try:
        from pybtex.database.input.bibtex import Parser
        from pybtex.database.output.bibtex import Writer
        from pybtex.database import BibliographyData, PybtexError
        from pybtex.backends import html
        from pybtex.style.formatting import plain
    except ImportError:
        logger.warn('`pelican_bibtex` failed to load dependency `pybtex`')
        return

    refs_file = generator.settings['PUBLICATIONS_SRC']
    try:
        bibdata_all = Parser().parse_file(refs_file)
    except PybtexError as e:
        logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
            refs_file,
            str(e)))
        return

    publications = []

    # format entries
    plain_style = plain.Style()
    html_backend = html.Backend()
    formatted_entries = plain_style.format_entries(bibdata_all.entries.values())

    for formatted_entry in formatted_entries:
        key = formatted_entry.key
        entry = bibdata_all.entries[key]
        year = entry.fields.get('year')

        authors = entry.fields.get('author').split(' and ')
        authors = [(x.split(',')[1] + ' ' + x.split(',')[0]).strip() for x in authors]

        title = entry.fields.get('title')
        # This shouldn't really stay in the field dict
        # but new versions of pybtex don't support pop
        pdf = entry.fields.get('pdf', None)
        slides = entry.fields.get('slides', None)
        poster = entry.fields.get('poster', None)

        #render the bibtex string for the entry
        bib_buf = StringIO()
        bibdata_this = BibliographyData(entries={key: entry})
        Writer().write_stream(bibdata_this, bib_buf)
        text = formatted_entry.text.render(html_backend)

        publications.append((key,
                             title,
                             year,
                             authors,
                             pdf,
                             slides,
                             poster))

    return publications


from pelican.generators import Generator, CachingGenerator
from pelican.readers import BaseReader
from pelican.utils import *
import os

class BibGenerator(Generator):
    enabled = True

    def __init__(self, *args, **kwargs):
        logger.info('-------> INIT INVOKED')
        self.publications = []
        super(BibGenerator, self).__init__(*args, **kwargs)
        signals.generator_init.send(self)

    def generate_context(self):
        logger.info('-------> GENERATE_CONTEXT INVOKED')
        publications = add_publications(self)
        self.context['publications'] = publications
        self.publications = publications
        #signals.finalized.send(self)

    def generate_publications(self, write):
        publication_template = self.get_template('publication')
        for key, title, year, authors, pdf, slides, poster in self.publications:
            write('publications/{}.html'.format(key), publication_template, self.context)

    def generate_output(self, writer):
        x = self.settings['PUBLICATIONS_SRC']
        logger.info('-------> GENERATE_OUTPUT INVOKED ' + x)
        write = partial(writer.write_file,
                        relative_urls=self.settings['RELATIVE_URLS'])
        self.generate_publications(write)

def get_bib_generator(generator):
    # define a new generator here if you need to
    settings = generator.settings
    return BibGenerator

def register():
    #signals.generator_init.connect(add_publications)
    signals.get_generators.connect(get_bib_generator)

"""
class ArticlesGenerator(CachingGenerator):

    def __init__(self, *args, **kwargs):
        self.articles = []  # only articles in default language
        self.translations = []
        self.dates = {}
        self.tags = defaultdict(list)
        self.categories = defaultdict(list)
        self.related_posts = []
        self.authors = defaultdict(list)
        self.drafts = [] # only drafts in default language
        self.drafts_translations = []
        super(ArticlesGenerator, self).__init__(*args, **kwargs)
        signals.article_generator_init.send(self)

    def generate_feeds(self, writer):

        if self.settings.get('FEED_ATOM'):
            writer.write_feed(self.articles, self.context,
                              self.settings['FEED_ATOM'])

        if self.settings.get('FEED_RSS'):
            writer.write_feed(self.articles, self.context,
                              self.settings['FEED_RSS'], feed_type='rss')

        if (self.settings.get('FEED_ALL_ATOM')
                or self.settings.get('FEED_ALL_RSS')):
            all_articles = list(self.articles)
            for article in self.articles:
                all_articles.extend(article.translations)
            all_articles.sort(key=attrgetter('date'), reverse=True)

            if self.settings.get('FEED_ALL_ATOM'):
                writer.write_feed(all_articles, self.context,
                                  self.settings['FEED_ALL_ATOM'])

            if self.settings.get('FEED_ALL_RSS'):
                writer.write_feed(all_articles, self.context,
                                  self.settings['FEED_ALL_RSS'],
                                  feed_type='rss')

        for cat, arts in self.categories:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('CATEGORY_FEED_ATOM'):
                writer.write_feed(arts, self.context,
                                  self.settings['CATEGORY_FEED_ATOM']
                                  % cat.slug)

            if self.settings.get('CATEGORY_FEED_RSS'):
                writer.write_feed(arts, self.context,
                                  self.settings['CATEGORY_FEED_RSS']
                                  % cat.slug, feed_type='rss')

        for auth, arts in self.authors:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('AUTHOR_FEED_ATOM'):
                writer.write_feed(arts, self.context,
                                  self.settings['AUTHOR_FEED_ATOM']
                                  % auth.slug)

            if self.settings.get('AUTHOR_FEED_RSS'):
                writer.write_feed(arts, self.context,
                                  self.settings['AUTHOR_FEED_RSS']
                                  % auth.slug, feed_type='rss')

        if (self.settings.get('TAG_FEED_ATOM')
                or self.settings.get('TAG_FEED_RSS')):
            for tag, arts in self.tags.items():
                arts.sort(key=attrgetter('date'), reverse=True)
                if self.settings.get('TAG_FEED_ATOM'):
                    writer.write_feed(arts, self.context,
                                      self.settings['TAG_FEED_ATOM']
                                      % tag.slug)

                if self.settings.get('TAG_FEED_RSS'):
                    writer.write_feed(arts, self.context,
                                      self.settings['TAG_FEED_RSS'] % tag.slug,
                                      feed_type='rss')

        if (self.settings.get('TRANSLATION_FEED_ATOM')
                or self.settings.get('TRANSLATION_FEED_RSS')):
            translations_feeds = defaultdict(list)
            for article in chain(self.articles, self.translations):
                translations_feeds[article.lang].append(article)

            for lang, items in translations_feeds.items():
                items.sort(key=attrgetter('date'), reverse=True)
                if self.settings.get('TRANSLATION_FEED_ATOM'):
                    writer.write_feed(
                        items, self.context,
                        self.settings['TRANSLATION_FEED_ATOM'] % lang)
                if self.settings.get('TRANSLATION_FEED_RSS'):
                    writer.write_feed(
                        items, self.context,
                        self.settings['TRANSLATION_FEED_RSS'] % lang,
                        feed_type='rss')

    def generate_articles(self, write):
        for article in chain(self.translations, self.articles):
            signals.article_generator_write_article.send(self, content=article)
            write(article.save_as, self.get_template(article.template),
                  self.context, article=article, category=article.category,
                  override_output=hasattr(article, 'override_save_as'),
                  blog=True)

    def generate_period_archives(self, write):
        try:
            template = self.get_template('period_archives')
        except PelicanTemplateNotFound:
            template = self.get_template('archives')

        period_save_as = {
            'year': self.settings['YEAR_ARCHIVE_SAVE_AS'],
            'month': self.settings['MONTH_ARCHIVE_SAVE_AS'],
            'day': self.settings['DAY_ARCHIVE_SAVE_AS'],
        }

        period_date_key = {
            'year': attrgetter('date.year'),
            'month': attrgetter('date.year', 'date.month'),
            'day': attrgetter('date.year', 'date.month', 'date.day')
        }

        def _generate_period_archives(dates, key, save_as_fmt):
            # `dates` is already sorted by date
            for _period, group in groupby(dates, key=key):
                archive = list(group)
                # arbitrarily grab the first date so that the usual
                # format string syntax can be used for specifying the
                # period archive dates
                date = archive[0].date
                save_as = save_as_fmt.format(date=date)
                context = self.context.copy()

                if key == period_date_key['year']:
                    context["period"] = (_period,)
                else:
                    month_name = calendar.month_name[_period[1]]
                    if not six.PY3:
                        month_name = month_name.decode('utf-8')
                    if key == period_date_key['month']:
                        context["period"] = (_period[0],
                                             month_name)
                    else:
                        context["period"] = (_period[0],
                                             month_name,
                                             _period[2])

                write(save_as, template, context,
                      dates=archive, blog=True)

        for period in 'year', 'month', 'day':
            save_as = period_save_as[period]
            if save_as:
                key = period_date_key[period]
                _generate_period_archives(self.dates, key, save_as)

    def generate_direct_templates(self, write):
        PAGINATED_TEMPLATES = self.settings['PAGINATED_DIRECT_TEMPLATES']
        for template in self.settings['DIRECT_TEMPLATES']:
            paginated = {}
            if template in PAGINATED_TEMPLATES:
                paginated = {'articles': self.articles, 'dates': self.dates}
            save_as = self.settings.get("%s_SAVE_AS" % template.upper(),
                                        '%s.html' % template)
            if not save_as:
                continue

            write(save_as, self.get_template(template),
                  self.context, blog=True, paginated=paginated,
                  page_name=os.path.splitext(save_as)[0])

    def generate_tags(self, write):
        tag_template = self.get_template('tag')
        for tag, articles in self.tags.items():
            articles.sort(key=attrgetter('date'), reverse=True)
            dates = [article for article in self.dates if article in articles]
            write(tag.save_as, tag_template, self.context, tag=tag,
                  articles=articles, dates=dates,
                  paginated={'articles': articles, 'dates': dates}, blog=True,
                  page_name=tag.page_name, all_articles=self.articles)

    def generate_categories(self, write):
        category_template = self.get_template('category')
        for cat, articles in self.categories:
            articles.sort(key=attrgetter('date'), reverse=True)
            dates = [article for article in self.dates if article in articles]
            write(cat.save_as, category_template, self.context,
                  category=cat, articles=articles, dates=dates,
                  paginated={'articles': articles, 'dates': dates}, blog=True,
                  page_name=cat.page_name, all_articles=self.articles)

    def generate_authors(self, write):
        author_template = self.get_template('author')
        for aut, articles in self.authors:
            articles.sort(key=attrgetter('date'), reverse=True)
            dates = [article for article in self.dates if article in articles]
            write(aut.save_as, author_template, self.context,
                  author=aut, articles=articles, dates=dates,
                  paginated={'articles': articles, 'dates': dates}, blog=True,
                  page_name=aut.page_name, all_articles=self.articles)

    def generate_drafts(self, write):
        for draft in chain(self.drafts_translations, self.drafts):
            write(draft.save_as, self.get_template(draft.template),
                self.context, article=draft, category=draft.category,
                override_output=hasattr(draft, 'override_save_as'),
                blog=True, all_articles=self.articles)

    def generate_pages(self, writer):
        write = partial(writer.write_file,
                        relative_urls=self.settings['RELATIVE_URLS'])

        # to minimize the number of relative path stuff modification
        # in writer, articles pass first
        self.generate_articles(write)
        self.generate_period_archives(write)
        self.generate_direct_templates(write)

        # and subfolders after that
        self.generate_tags(write)
        self.generate_categories(write)
        self.generate_authors(write)
        self.generate_drafts(write)

    def generate_context(self):

        all_articles = []
        all_drafts = []
        for f in self.get_files(
                self.settings['ARTICLE_PATHS'],
                exclude=self.settings['ARTICLE_EXCLUDES']):
            article_or_draft = self.get_cached_data(f, None)
            if article_or_draft is None:
            #TODO needs overhaul, maybe nomad for read_file solution, unified behaviour
                try:
                    article_or_draft = self.readers.read_file(
                        base_path=self.path, path=f, content_class=Article,
                        context=self.context,
                        preread_signal=signals.article_generator_preread,
                        preread_sender=self,
                        context_signal=signals.article_generator_context,
                        context_sender=self)
                except Exception as e:
                    logger.error('Could not process %s\n%s', f, e,
                        exc_info=self.settings.get('DEBUG', False))
                    self._add_failed_source_path(f)
                    continue

                if not is_valid_content(article_or_draft, f):
                    self._add_failed_source_path(f)
                    continue

                if article_or_draft.status.lower() == "published":
                    all_articles.append(article_or_draft)
                elif article_or_draft.status.lower() == "draft":
                    article_or_draft = self.readers.read_file(
                        base_path=self.path, path=f, content_class=Draft,
                        context=self.context,
                        preread_signal=signals.article_generator_preread,
                        preread_sender=self,
                        context_signal=signals.article_generator_context,
                        context_sender=self)
                    self.add_source_path(article_or_draft)
                    all_drafts.append(article_or_draft)
                else:
                    logger.error("Unknown status '%s' for file %s, skipping it.",
                                   article_or_draft.status, f)
                    self._add_failed_source_path(f)
                    continue

                self.cache_data(f, article_or_draft)

            self.add_source_path(article_or_draft)


        self.articles, self.translations = process_translations(all_articles,
                order_by=self.settings['ARTICLE_ORDER_BY'])
        self.drafts, self.drafts_translations = \
            process_translations(all_drafts)

        signals.article_generator_pretaxonomy.send(self)

        for article in self.articles:
            # only main articles are listed in categories and tags
            # not translations
            self.categories[article.category].append(article)
            if hasattr(article, 'tags'):
                for tag in article.tags:
                    self.tags[tag].append(article)
            for author in getattr(article, 'authors', []):
                self.authors[author].append(article)

        self.dates = list(self.articles)
        self.dates.sort(key=attrgetter('date'),
                        reverse=self.context['NEWEST_FIRST_ARCHIVES'])

        # and generate the output :)

        # order the categories per name
        self.categories = list(self.categories.items())
        self.categories.sort(
            reverse=self.settings['REVERSE_CATEGORY_ORDER'])

        self.authors = list(self.authors.items())
        self.authors.sort()

        self._update_context(('articles', 'dates', 'tags', 'categories',
                              'authors', 'related_posts', 'drafts'))
        self.save_cache()
        self.readers.save_cache()
        signals.article_generator_finalized.send(self)

    def generate_output(self, writer):
        self.generate_feeds(writer)
        self.generate_pages(writer)
        signals.article_writer_finalized.send(self, writer=writer)
"""