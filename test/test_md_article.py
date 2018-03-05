import logging
logger = logging.getLogger(__name__)

import os
import codecs

from pelican.readers import MarkdownReader
from pelican.settings import DEFAULT_CONFIG


ARTICLE_DIR = 'content/articles'

# Iterate over all files in ARTICLE_DIR (recursively with walk)
# and try parsing them with pelicans' MarkdownReader
md_reader = MarkdownReader(DEFAULT_CONFIG)
for dirpath, subdirs, files in os.walk(ARTICLE_DIR):
    for file in files:
        logger.warn( '[MD] Trying to parse {}...'.format(file))
        path = os.path.join(dirpath, file)
        md_reader.read(path)