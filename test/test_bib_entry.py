import logging
logger = logging.getLogger(__name__)

import os
import codecs

from pybtex.database.input.bibtex import Parser

PUBLICATION_DIR = 'content/publications'

# Iterate over all the files in the PUBLICATION_DIR
for file in os.listdir(PUBLICATION_DIR):
    logger.warn( '[BIB] Trying to parse {}...'.format(file))
    # Try parsing it, should not crash
    with codecs.open(PUBLICATION_DIR+os.sep+file, 'r', encoding="utf8") as stream:
        assert len(stream.read()) > 0 
        bibdata = Parser().parse_stream(stream)