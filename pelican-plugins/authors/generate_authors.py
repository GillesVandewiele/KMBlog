from pelican import signals
from pelican.urlwrappers import Author

def add_missing_authors(generator):
    # AUTHORS defined in pelicanconf
    # presumably an iterator with string keys/items as author names
    authors = generator.settings.get('AUTHORS', {})
    added_authors = set(author.name for author, articles in generator.authors)
    for author in set(authors)-added_authors:
        generator.authors.append((Author(author, generator.settings), []))

def register():
    signals.article_generator_finalized.connect(add_missing_authors)