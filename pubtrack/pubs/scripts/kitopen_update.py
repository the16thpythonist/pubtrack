"""
A script which will attempt to update publications on a pubtrack instance with KITOpen specific information, such as
the KITOpen ID or the funding information in form of the POF structure.

The script does not requires any input. The parameters of the script can be modified by changing the values of the
relevant constants in code here.
"""
import os
import logging

from pykitopen import KitOpen
from pykitopen.search import YearBatching
from pykitopen.publication import Publication
from pykitopen.config import DEFAULT as KITOPEN_DEFAULT

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT as PUBTRACK_DEFAULT

# DEFINING THE IMPORTANT CONSTANTS
# --------------------------------

LOG_PATH = '/tmp/pubtrack_kitopen_update.log'

PUBTRACK_URL = "http://pubtrack.ignorelist.com/api/v1"
PUBTRACK_TOKEN = "573e32eef8489a17eb9f448901d75fe1426eb610"

START_YEAR = '2018'

# SETTING UP LOGGING
# ------------------

logger = logging.getLogger('KITOpen Update')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(filename=LOG_PATH, mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# SETTING UP KITOPEN WRAPPER
# --------------------------

kitopen_config = KITOPEN_DEFAULT.copy()
kitopen_config['default_view'] = Publication.VIEWS.FULL
kitopen_config['batching_strategy'] = YearBatching

kitopen = KitOpen(kitopen_config)

# SETTING UP PUBTRACK WRAPPER
# ---------------------------

pubtrack_config = PUBTRACK_DEFAULT.copy()
pubtrack_config['url'] = PUBTRACK_URL
pubtrack_config['token'] = PUBTRACK_TOKEN

pubtrack = Pubtrack(pubtrack_config)

# HELPER CLASSES/METHODS
# ----------------------


def name_search_string(first_name: str, last_name: str):
    """
    Given the first name and the last name of an author, creates a search string for the KITOpen data base from those

    :param first_name:
    :param last_name:
    :return:
    """
    return f'{last_name.upper()}, {first_name[0].upper()}*'

# ACTUAL EXECUTION
# ----------------


logger.info('FETCHING META AUTHORS FROM PUBTRACK')
AUTHOR_NAMES = []
meta_authors = pubtrack.meta_author.get()['results']
for meta_author in meta_authors:
    for author in meta_author['authors']:
        name = name_search_string(author['first_name'], author['last_name'])
        AUTHOR_NAMES.append(name)
        logger.info(' * Adding author name {}'.format(name))

logger.info('==> Processing total of {} authors'.format(len(AUTHOR_NAMES)))


results = kitopen.search({
    'author':       ' or '.join(AUTHOR_NAMES),
    'start':        START_YEAR,
    'end':          ''
})

logger.info('FETCHING PUBLICATIONS FROM KITOPEN')
count = 0
count_success = 0
for publication in results:

    if publication.data['doi']:
        try:
            pub = pubtrack.publication.get_by(doi=publication.data['doi'])
            patch = {
                'on_kitopen':           True,
                'pof_structure':        publication.data['pof_structure']
            }
            if not pub['kitopen_id']:
                patch['kitopen_id'] = publication.data['id']

            pubtrack.publication.patch(pub['uuid'], patch=patch)
            logger.info(' * UPDATED publication {}'.format(publication.data['doi']))
            count_success += 1
        except Exception as e:
            logger.error(' ! Warning updating publication {}: "{}"'.format(publication.data['doi'], str(e)))
        finally:
            count += 1

logger.info(' ==> Updated {}/{} publications with KITOpen data'.format(count_success, count))