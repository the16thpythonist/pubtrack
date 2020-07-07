"""
A script, which will import publications from the scopus database to a PubTrack instance, based on a list of scopus
author ids from the observed authors.

The script does not requires any input. The parameters of the script can be modified by changing the values of the
relevant constants in code here.
"""
import datetime

import pybliometrics
from pybliometrics.scopus import AbstractRetrieval, ScopusSearch
from pybliometrics.scopus import config as scopus_config

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT as PUBTRACK_DEFAULT


# DEFINING THE IMPORTANT CONSTANTS
# --------------------------------

PUBTRACK_URL = "http://0.0.0.0:8000/api/v1"
PUBTRACK_TOKEN = "7313f9788f8d1543a78bdaacc7da8f610db0eb1c"

SCOPUS_API_KEY = "013ff70c81049af047c0648e87278a9a"

SINCE = 2019
AUTHOR_LIMIT = 5
AUTHORS = ['35313939900']

# SETTING UP SCOPUS WRAPPER
# -------------------------

# We need to consider the case that this is the first execution and no config exists on the local machine
# but in any way we will set the api key defined above into the config
try:
    pybliometrics.scopus.utils.create_config()
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
        return "2020-06-14T14:07:38+0000"


# FETCHING THE ACTUAL PUBLICATIONS
# --------------------------------

meta_authors = pubtrack.meta_authors.get()
RELEVANT_AUTHOR_IDS = AUTHORS.copy()
DATE_LIMIT = datetime.datetime(year=SINCE, month=1, day=1)

for author_id in AUTHORS:
    publication_count = 0
    search = ScopusSearch(f'AU-ID ( {author_id} )')
    print(f'\n--- STARTING SEARCH FOR AUTHOR {author_id} ---')

    for result in search.results:

        # We'll only take publications, which have a DOI
        if result.doi is None: continue

        # Requesting the detailed information from the scopus database for the current publication from the search
        # results
        try:
            abstract_retrieval = AbstractRetrieval(result.doi)
        except:
            print(f' [!] ERROR Could not get details for publication {result.doi}')
            continue

        # If the publication is older than the date limit, it will be discarded
        print(abstract_retrieval.coverDate)
        # if abstract_retrieval.coverDate <= DATE_LIMIT:
        #     continue

        adapter = ScopusPublicationAdapter(abstract_retrieval)
        publication = adapter.get_publication()

        # Filtering the authors according to the AUTHOR_LIMIT, which has been set.
        # We cannot just use the first few authors however, we need to make sure that the author, from which we have
        # this publication in the first place is in there. The rest just gets filled up...
        authors = []
        for author in publication['authors']:
            if author['scopus_id'] in RELEVANT_AUTHOR_IDS or len(authors) < AUTHOR_LIMIT:
                authors.append(author)

        publication['authors'] = authors

        # Now we try to actually POST the publication to the pubtrack REST API
        try:
            pubtrack.import_publication(publication)
            publication_count += 1
            print(f' * Publication "{publication["doi"]}" success!')
        except Exception as e:
            print(f' [!] ERROR while posting to pubtrack "{str(e)}"')
            continue

    print(f'--> Total of {publication_count} Publications imported for author {author_id}')

