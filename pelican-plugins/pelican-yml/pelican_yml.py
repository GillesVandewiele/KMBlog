class YMLGenerator(Generator):
    enabled = True

    def __init__(self, *args, **kwargs):
        self.conferences = []
        self.conferences_per_type = {}
        super(YMLGenerator, self).__init__(*args, **kwargs)
        signals.generator_init.send(self)

    def add_publications(self):
        # Check if PUBLICATIONS_SRC is set
        if 'CONFERENCES_SRC' not in self.settings or 'CONFERENCES_TYPES' not in self.settings:
            logger.warn('Make sure both CONFERENCES_SRC and CONFERENCES_TYPES are set.')
            return

        """
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

        """
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