"""
A script which will attempt to update publications on a pubtrack instance with KITOpen specific information, such as
the KITOpen ID or the funding information in form of the POF structure.

The script does not requires any input. The parameters of the script can be modified by changing the values of the
relevant constants in code here.
"""
from pykitopen import KitOpen
from pykitopen.publication import Publication
from pykitopen.config import DEFAULT as KITOPEN_DEFAULT

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT as PUBTRACK_DEFAULT

# DEFINING THE IMPORTANT CONSTANTS
# --------------------------------

PUBTRACK_URL = "http://0.0.0.0:8000/api/v1"
PUBTRACK_TOKEN = "7313f9788f8d1543a78bdaacc7da8f610db0eb1c"

START_YEAR = '2018'

# SETTING UP KITOPEN WRAPPER
# --------------------------

kitopen_config = KITOPEN_DEFAULT.copy()
kitopen_config['default_view'] = Publication.VIEWS.FULL

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


print('\n--- FETCHING META AUTHORS FROM PUBTRACK ---')
AUTHOR_NAMES = []
meta_authors = pubtrack.meta_authors.get()
for meta_author in meta_authors:
    for author in meta_author['authors']:
        name = name_search_string(author['first_name'], author['last_name'])
        print(f' * {name}')
        AUTHOR_NAMES.append(name)
print(f'--> Total of {len(AUTHOR_NAMES)} to be queried from KITOpen')


results = kitopen.search({
    'author':       ' or '.format(AUTHOR_NAMES),
    'start':        START_YEAR,
    'end':          ''
})

print('\n--- FETCHING PUBLICATIONS FROM KITOPEN ---')
for publication in results:

    if publication.data['doi']:
        try:
            pub = pubtrack.publication.get(doi=publication.data['doi'])
            patch = {
                'on_kitopen':           True,
                'kitopen_id':           publication.data['id'],
                'pof_structure':        publication.data['pof_structure']
            }
            pubtrack.publication.patch(pub['uuid'], patch=patch)
            print(f' * Inserted publication {publication.data["doi"]} imported to pubtrack')
        except:
            print(f' [!] Error importing publication {publication.data["doi"]}')