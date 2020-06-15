# %%

import os
import json

from typing import Iterable
from collections import namedtuple
from urllib.parse import urljoin

import requests

# %%

URL = "http://0.0.0.0:8000/api/v1"
VERBOSE = True

TOKEN = "02d7341b9e6efb56b1d4b7b3981975d64f12b7a4"
HEADERS = {
    'Authorization': f'Token {TOKEN}'
}

AUTHORS_URL = os.path.join(URL, 'authors/')
PUBLICATIONS_URL = os.path.join(URL, 'publications/')
AUTHORINGS_URL = os.path.join(URL, 'authorings/')
AFFILIATIONS_URL = os.path.join(URL, 'affiliations/')
META_AUTHORS_URL = os.path.join(URL, 'meta-authors/')
BLACKLISTINGS_URL = os.path.join(URL, 'blacklistings/')
INSTITUTIONS_URL = os.path.join(URL, 'institutions/')


# %%

def exclude_keys(d: dict, keys: Iterable):
    copy = d.copy()
    for key in keys:
        del copy[key]

    return copy


# %%

def post_author(author: dict):
    # print(json.dumps(author))
    return requests.post(
        AUTHORS_URL,
        json=author,
        headers=HEADERS
    )


def get_author_by_scopus(scopus_id: str):
    response = requests.get(
        AUTHORS_URL,
        params={
            'scopus_id': scopus_id
        },
        headers=HEADERS
    )
    content = response.json()
    if len(content['results']) != 0:
        return content['results'][0]
    else:
        return None


def put_author(slug: str, author: dict):
    url = os.path.join(AUTHORS_URL, f'{slug}/')
    return requests.put(
        url,
        json=author,
        headers=HEADERS
    )


def post_publication(publication: dict):
    return requests.post(
        PUBLICATIONS_URL,
        json=publication,
        headers=HEADERS
    )


def get_publication_by_scopus(scopus_id: str):
    response = requests.get(
        PUBLICATIONS_URL,
        params={
            'scopus_id': scopus_id
        },
        headers=HEADERS
    )
    content = response.json()
    return content['results'][0] if len(content['results']) != 0 else None


def post_authoring(authoring: dict):
    return requests.post(
        AUTHORINGS_URL,
        json=authoring,
        headers=HEADERS
    )


def post_meta_author(meta_author: dict):
    return requests.post(
        META_AUTHORS_URL,
        json=meta_author,
        headers=HEADERS
    )


def post_affiliation(affiliation: dict):
    return requests.post(
        AFFILIATIONS_URL,
        json=affiliation,
        headers=HEADERS
    )


def post_blacklisting(blacklisting: dict):
    return requests.post(
        BLACKLISTINGS_URL,
        json=blacklisting,
        headers=HEADERS
    )


def post_institution(institution: dict):
    return requests.post(
        INSTITUTIONS_URL,
        json=institution,
        headers=HEADERS
    )


def get_institution_by_scopus(scopus_id: str):
    response = requests.get(
        INSTITUTIONS_URL,
        params={
            'scopus_id': scopus_id
        },
        headers=HEADERS
    )
    content = response.json()
    if len(content['results']) != 0:
        return content['results'][0]
    else:
        return None


# %%

def insert_meta_author(meta_author: dict):
    base = exclude_keys(meta_author, ['authors', 'blacklisted_institutions'])
    response = post_meta_author(base)
    if VERBOSE: print(response.content, response.status_code)

    if response.status_code != 201:
        return

    meta_author_data = response.json()
    # POST-ing all the authors associated with the meta author
    for author in meta_author['authors']:
        author['meta_author'] = {
            'slug': meta_author_data['slug']
        }
        response = post_author(author)

        # If the author already exists we need to edit it to reference the meta
        # author
        if response.status_code == 400:
            author_data = get_author_by_scopus(author['scopus_id'])
            if author_data:
                response = put_author(author_data['slug'], author_data)
                if VERBOSE: print(response.content, response.status_code)

    # POST-ing all the institutions which should be blacklisted
    for institution in meta_author['blacklisted_institutions']:
        response = post_institution(institution)
        institution_data = None

        if response.status_code == 201:
            institution_data = response.json()

        if response.status_code == 400:
            institution_data = get_institution_by_scopus(institution['scopus_id'])

        # Creating a new blacklisting
        if institution_data:
            blacklisting = {
                'meta_author': meta_author_data['slug'],
                'institution': institution_data['slug']
            }
            post_blacklisting(blacklisting)


# %%

def insert_publication(publication: dict):
    base = exclude_keys(publication, ['authors'])
    response = post_publication(base)
    if VERBOSE: print(response.content, response.status_code)

    if response.status_code == 201:
        publication_data = response.json()
    else:
        publication_data = get_publication_by_scopus(publication['scopus_id'])

    if not publication_data:
        return

    # POST-ing all the authors for this publication
    for author in publication['authors']:
        response = post_author(author)
        author_data = None
        if VERBOSE: print(response.content, response.status_code)

        if response.status_code == 201:
            author_data = response.json()

        if response.status_code == 400:
            author_data = get_author_by_scopus(author['scopus_id'])

        if author_data:
            authoring = {
                'author': author_data['slug'],
                'publication': publication_data['uuid']
            }
            response = post_authoring(authoring)
            if VERBOSE: print(response.content, response.status_code)


# %%

# Possible authors to choose from
AUTHORS_DICT = {
    'martin': {
        'first_name': 'Martin',
        'last_name': 'Seeberg',
        'scopus_id': '1'
    },
    'daniela': {
        'first_name': 'Daniela',
        'last_name': 'Hundt',
        'scopus_id': '2'
    },
    'liu': {
        'first_name': 'Liu',
        'last_name': 'Cixin',
        'scopus_id': '3'
    },
    'jonas1': {
        'first_name': 'Jonas',
        'last_name': 'Teufel',
        'scopus_id': '4'
    },
    'jonas2': {
        'first_name': 'Jonas',
        'last_name': 'Teuvel',
        'scopus_id': '5'
    },
    'peter': {
        'first_name': 'Peter',
        'last_name': 'Silie',
        'scopus_id': '6'
    },
    'adam': {
        'first_name': 'Adam',
        'last_name': 'Riese',
        'scopus_id': '7'
    },
    'dagobert': {
        'first_name': 'Dagobert',
        'last_name': 'Duck',
        'scopus_id': '8'
    },
    'frank': {
        'first_name': 'Frank',
        'last_name': 'Rosin',
        'scopus_id': '9'
    },
    'john1': {
        'first_name': 'John',
        'last_name': 'Doe',
        'scopus_id': '10'
    },
    'john2': {
        'first_name': 'John',
        'last_name': 'Moe',
        'scopus_id': '11'
    }
}

POF_STRUCTURES_DICT = {
    'ipe': 'IPE.2129.rest',
    'aug': 'AUG.298.190.sf',
}

META_AUTHORS_DICT = {
    'jonas': {
        'first_name': 'Jonas',
        'last_name': 'Teufel',
        'slug': 'jonas-teufel',
        'authors': [
            AUTHORS_DICT['jonas1'],
            AUTHORS_DICT['jonas2']
        ],
        'blacklisted_institutions': []
    },
    'john': {
        'first_name': 'John',
        'last_name': 'Doe',
        'slug': 'john-doe',
        'authors': [
            AUTHORS_DICT['john1'],
            AUTHORS_DICT['john2']
        ],
        'blacklisted_institutions': []
    }
}

PUBLICATIONS_LIST = [
    {
        'title': 'Some Experiment!',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '1',
        'on_kitopen': False,
        'authors': [
            AUTHORS_DICT['martin'],
            AUTHORS_DICT['daniela']
        ]
    },
    {
        'title': 'Mixing Fire and Explosives makes BOOooMM!',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '2',
        'on_kitopen': False,
        'authors': [
            AUTHORS_DICT['dagobert'],
            AUTHORS_DICT['daniela']
        ]
    },
    {
        'title': 'Wow, huge collaboration',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '3',
        'on_kitopen': True,
        'kitopen_id': '1',
        'pof_strcuture': POF_STRUCTURES_DICT['ipe'],
        'authors': [
            AUTHORS_DICT['dagobert'],
            AUTHORS_DICT['daniela'],
            AUTHORS_DICT['john1'],
            AUTHORS_DICT['jonas2'],
            AUTHORS_DICT['adam']
        ]
    },
    {
        'title': 'How to make a low-pass filter',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '4',
        'on_kitopen': True,
        'kitopen_id': '2',
        'pof_structure': POF_STRUCTURES_DICT['ipe'],
        'authors': [
            AUTHORS_DICT['jonas1'],
            AUTHORS_DICT['adam']
        ]
    },
    {
        'title': 'Investigating space-time wormholes',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '5',
        'on_kitopen': True,
        'kitopen_id': '3',
        'pof_structure': POF_STRUCTURES_DICT['aug'],
        'authors': [
            AUTHORS_DICT['john1'],
            AUTHORS_DICT['liu']
        ]
    },
    {
        'title': 'Why is milk white?',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '6',
        'on_kitopen': False,
        'authors': [
            AUTHORS_DICT['daniela'],
            AUTHORS_DICT['martin'],
            AUTHORS_DICT['frank']
        ]
    },
    {
        'title': 'Building a time machine 101',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '7',
        'on_kitopen': False,
        'authors': [
            AUTHORS_DICT['jonas1'],
            AUTHORS_DICT['john1'],
            AUTHORS_DICT['peter']
        ]
    },
    {
        'title': 'Brewing beer with dynamite',
        'published': '2020-05-25T12:33:46+0000',
        'scopus_id': '8',
        'on_kitopen': False,
        'authors': [
            AUTHORS_DICT['martin']
        ]
    }
]

# %%

for meta_author in META_AUTHORS_DICT.values():
    insert_meta_author(meta_author)

for publication in PUBLICATIONS_LIST:
    insert_publication(publication)
