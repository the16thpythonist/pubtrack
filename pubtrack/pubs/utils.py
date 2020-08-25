"""
A module containing various utility functions, which semantically do not belong anywhere else.
"""
import random
import string
import os

"""
:var ALPHANUMERIC_CHARS: This is a list of all characters, which are either lower case ASCII characters of digits.
                         Effectively this is a subset of the allowed characters for the usage within slugs. This list 
                         will be needed for the creation of random strings.
"""
ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits

# Since these URLS may be subject to change it would be better to move them to the settings. There they could be set
# as default values, but could also be changed by the user in case they have to!
KITOPEN_URL = "https://publikationen.bibliothek.kit.edu"
SCOPUS_URL = "https://scopus.com/record"
DOI_URL = "https://doi.org"


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=6):
    """
    Generates a random string using the given list of characters *char* and of the given *length*.

    :param chars: The character set from which to draw from for the creation of the random string
    :param length:

    :type chars: A list of characters, more specifically a list of strings with the length 1
    :type length: int

    :return: A random string
    """
    # I must admit I have this line of code from the Internet, but it is quite ingenious.
    # You create a list of random choices from the available characters in a list comprehension and then join this
    # into a string. I could not have done it this elegantly.
    return "".join(random.choice(chars) for _ in range(length))


"""
**A note on the URL wrapper functions**

I want to explain the design choice for these functions which simply wrap the creation of a URL for the different 
other websites to display the publications. Right now two of these three functions literally just join together the 
base url and the parameter. One could argue, that this code could have been used directly where it is needed, but I 
think it is quite important to wrap this in a function for the following reasons:
- The way these URLs of the 3rd party websites work may be subject to change and changing it all here ar a universal
  position instead of all over the code would be easier.
- One of these websites does indeed work differently and having them all be coded the same way is more intuitive.
I find it important to follow this principle of trying to foresee future changes in circumstances and thus loosly 
coupling code.
"""


def get_scopus_url(eid: str) -> str:
    """
    Given the eid of a publication, returns the URL to access that on the Scopus website.

    :param eid: The EID of the publication to display on scopus

    :type eid: str

    :return:
    """
    tail = f'display.uri?eid={eid}&origin=resultslist'
    return os.path.join(SCOPUS_URL, tail)


def get_doi_url(doi: str) -> str:
    """
    Given the doi of a publication, returns the URL to display the details page of this publication.

    :param doi: The DOI of a publication to display

    :type doi: str

    :return:
    """
    return os.path.join(DOI_URL, doi)


def get_kitopen_url(kitopen_id: str) -> str:
    """
    Given the kitopen id of a publication, returns the url to display that publication on the KITOpen website.

    :param kitopen_id: The kitopen id of the publication

    :type kitopen_id: str

    :return:
    """
    return os.path.join(KITOPEN_URL, kitopen_id)