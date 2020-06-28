#%%

from pypubtrack import Pubtrack
from pypubtrack.config import DEFAULT

PUBTRACK_CONFIG = DEFAULT.copy()
PUBTRACK_CONFIG['token'] = '1e3defbbe5b559413b5e45ab984c72676c948a8b'
PUBTRACK_CONFIG['url'] = 'http://0.0.0.0:8000/api/v1'

pubtrack = Pubtrack(PUBTRACK_CONFIG)
print(pubtrack.meta_author.get())
