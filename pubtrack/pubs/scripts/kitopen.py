
from pykitopen import KitOpen
from pykitopen.config import DEFAULT as KITOPEN_DEFAULT
from pykitopen.publication import Publication

kitopen = KitOpen(KITOPEN_DEFAULT)

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT as PUBTRACK_DEFAULT

PUBTRACK_CONFIG = PUBTRACK_DEFAULT.copy()
PUBTRACK_CONFIG['token'] = '7313f9788f8d1543a78bdaacc7da8f610db0eb1c'
PUBTRACK_CONFIG['url'] = 'http://0.0.0.0:8000/api/v1'

pubtrack = Pubtrack(PUBTRACK_CONFIG)

# %%

meta_authors = pubtrack.meta_author.get('')['results']


def name(first, last):
    return f'{last.upper()}, {first[0].upper()}*'


NAMES = []
for meta_author in meta_authors:
    for author in meta_author['authors']:
        NAMES.append(name(author['first_name'], author['last_name']))

print(NAMES)

# %%

results = kitopen.search({
    'author': ' or '.join(NAMES),
    'start': '2018',
    'end': '2020'
})

for publication in results:
    doi = publication.data['doi']
    pof = publication.data['pof_structure']
    kitopen_id = publication.data['id']

    print(pof)

    if doi:
        pub = pubtrack.publication.get_by(doi=doi)
        pubtrack.publication.patch(
            pub['uuid'],
            patch={'pof_structure': pof, 'kitopen_id': kitopen_id, 'on_kitopen': True}
        )
        print(doi)