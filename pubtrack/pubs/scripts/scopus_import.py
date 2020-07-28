"""
A script, which will import publications from the scopus database to a PubTrack instance, based on a list of scopus
author ids from the observed authors.

The script does not requires any input. The parameters of the script can be modified by changing the values of the
relevant constants in code here.
"""
import os
import datetime
import logging
import pathlib

import pybliometrics
from pybliometrics.scopus import AbstractRetrieval, ScopusSearch
from pybliometrics.scopus import config as scopus_config

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT as PUBTRACK_DEFAULT


# DEFINING THE IMPORTANT CONSTANTS
# =============================================================================================
# ---------------------------------------------------------------------------------------------

PATH = pathlib.Path(__file__).parent.absolute()
LOG_PATH = '/tmp/pubtrack_scopus_import.log'

# PUBTRACK_URL = "http://pubtrack.ignorelist.com/api/v1"
# PUBTRACK_TOKEN = "573e32eef8489a17eb9f448901d75fe1426eb610"

PUBTRACK_URL = "http://0.0.0.0:8000/api/v1"
PUBTRACK_TOKEN = "46a79e91844078302272ceace5339ea40905adc1"

SCOPUS_API_KEY = "013ff70c81049af047c0648e87278a9a"

SINCE = 2019
AUTHOR_LIMIT = 5

# ---------------------------------------------------------------------------------------------
# =============================================================================================

# SETTING UP LOGGING
# ------------------

logger = logging.getLogger('Scopus Import')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(filename=LOG_PATH, mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# SETTING UP SCOPUS WRAPPER
# -------------------------

# We need to consider the case that this is the first execution and no config exists on the local machine
# but in any way we will set the api key defined above into the config
try:
    pybliometrics.scopus.utils.create_config()
except FileExistsError:
    pass
finally:
    scopus_config['Authentication']['APIKey'] = SCOPUS_API_KEY


# SETTING UP PUBTRACK WRAPPER
# ---------------------------

pubtrack_config = PUBTRACK_DEFAULT.copy()
pubtrack_config['url'] = PUBTRACK_URL
pubtrack_config['token'] = PUBTRACK_TOKEN

pubtrack = Pubtrack(pubtrack_config)


# HELPER METHODS/CLASSES
# ----------------------

class ScopusPublicationAdapter:

    def __init__(self, abstract_retrieval: AbstractRetrieval):
        self.abstract_retrieval = abstract_retrieval

    def get_publication(self):
        return {
            'title': self.abstract_retrieval.title,
            'published': self._convert_date(self.abstract_retrieval.coverDate),
            'doi': self.abstract_retrieval.doi,
            'scopus_id': self.abstract_retrieval.identifier,
            'authors': self.get_authors()
        }

    def get_authors(self):
        results = []
        for author in self.abstract_retrieval.authors:
            results.append({
                'first_name': author.given_name,
                'last_name': author.surname,
                'scopus_id': author.auid
            })
        return results

    def _convert_date(self, date: str):
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        return date_time.strftime('%Y-%m-%dT%H:%M:%S')


# FETCHING THE ACTUAL PUBLICATIONS
# --------------------------------

logger.info('FETCHING META AUTHORS FROM PUBTRACK')
AUTHORS = {}
meta_authors = pubtrack.meta_author.get()['results']
for meta_author in meta_authors:
    for author in meta_author['authors']:
        if author['scopus_id']:
            full_name = '{} {}'.format(author['first_name'], author['last_name'])
            AUTHORS[author['scopus_id']] = full_name
            logger.info(' * Adding author {}({}) to be processed'.format(full_name, author['scopus_id']))
logger.info('==> Processing total of {} authors'.format(len(AUTHORS)))


DATE_LIMIT = datetime.datetime(year=SINCE, month=1, day=1)

for author_id, full_name in AUTHORS.items():
    publication_count = 0
    search = ScopusSearch(f'AU-ID ( {author_id} )')
    logger.info('STARTING SEARCH FOR AUTHOR {}({})'.format(full_name, author_id))

    for result in search.results:

        # We'll only take publications, which have a DOI
        if result.doi is None:
            continue

        # Requesting the detailed information from the scopus database for the current publication from the search
        # results
        try:
            abstract_retrieval = AbstractRetrieval(result.doi)
        except Exception as e:
            logger.error(' ! Could not retrieve scopus abstract for DOI "{}". ERROR: {}'.format(result.doi, str(e)))
            continue

        # If the publication is older than the date limit, it will be discarded
        publication_date = datetime.datetime.strptime(abstract_retrieval.coverDate, '%Y-%m-%d')
        if publication_date <= DATE_LIMIT:
            logger.info(' # TOO OLD publication {} with publishing date {}'.format(result.doi, abstract_retrieval.coverDate))
            continue

        adapter = ScopusPublicationAdapter(abstract_retrieval)
        publication = adapter.get_publication()

        # Filtering the authors according to the AUTHOR_LIMIT, which has been set.
        # We cannot just use the first few authors however, we need to make sure that the author, from which we have
        # this publication in the first place is in there. The rest just gets filled up...
        authors = []
        for author in publication['authors']:
            if author['scopus_id'] in AUTHORS.keys() or len(authors) < AUTHOR_LIMIT:
                authors.append(author)

        publication['authors'] = authors

        # Now we try to actually POST the publication to the pubtrack REST API
        try:
            pubtrack.import_publication(publication)
            publication_count += 1
            logger.info(' * ADDED publication {}:{}'.format(publication['doi'], publication['title']))
        except Exception as e:
            logger.warning(' ! Error while posting to pubtrack: {}'.format(str(e)))
            continue

    logger.info(' --> Total of {} publications imported from author {}'.format(publication_count, author_id))

