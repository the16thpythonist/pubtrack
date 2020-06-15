import random
import string
import os

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits

# Maybe move this to the settings
KITOPEN_URL = ""
SCOPUS_URL = ""
DOI_URL = ""


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=6):
    return "".join(random.choice(chars) for _ in range(length))


def get_scopus_url(scopus_id: str) -> str:
    return os.path.join(SCOPUS_URL, scopus_id)


def get_doi_url(doi: str) -> str:
    return os.path.join(DOI_URL, doi)


def get_kitopen_url(kitopen_id: str) -> str:
    return os.path.join(KITOPEN_URL, kitopen_id)