"""
This module contains all the Models for this app

The objective of this app "pubs" is to provide a system for storing and accessing information about scientific
publications, their authors and other related data.

The models define the structure of the data, which is supposed to be managed by the app. Each model more or less
represents an object, which has multiple properties and methods. These objects will be persistently saved into the
sites database and can be queried to provide some sort of information to the REST interface and thus the frontend
user.
"""
from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
import uuid


"""
A NOTE ON THE SLUG FIELDS
Within this module some models have the field "slug", which has some peculiar settings: The field is set as the 
primary key of the database table, but it is also not editable and does not define a default value. Thus it should 
seem impossible to create a new object, because there is no way to define a slug, which will meet the requirements.

For most objects the slug will be created automatically from some other properties programmatically. This creation 
of the slug is implemented using django's "pre-save" signals. To see the concrete implementation visit the 
"signals.py" file of this package.
"""


class Institution(TimeStampedModel):
    """
    Represents a (scientific/research) institution.
    """

    slug = models.SlugField(max_length=255, unique=True, editable=False, primary_key=True)

    scopus_id = models.CharField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Returns the string representation of an institution.
        This will be the name of the inst. and the city where it is located in the brackets behind the name.

        :return:
        """
        return "{name} ({city})".format(
            name=self.name,
            city=self.city
        )


class Publication(TimeStampedModel):
    """
    Represents a research publication.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    title = models.CharField(max_length=255)
    published = models.DateTimeField(null=True)

    doi = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # SCOPUS RELATED FIELDS
    # ---------------------

    scopus_id = models.CharField(max_length=80, blank=True, null=True, unique=True)
    # 19.06.2020: So apparently you need the eid of a publication to access the scopus detail page of that publication
    eid = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # KITOPEN RELATED FIELDS
    # -----------------------

    on_kitopen = models.BooleanField(default=False)
    kitopen_id = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # The pof structure or "POF Struktur" is a KITOpen specific information. It defines to which project or rather
    # funding pool the publication belongs in the KIT internally.
    # This information is actually one of the most important ones, since this assignment is used to generate the
    # publication metrics for an institutes performance review!
    pof_structure = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return "{title}".format(
            title=self.title
        )


class PublicationStatus(TimeStampedModel):

    TYPE_WARNING = 'warn'
    TYPE_PERMITTED = 'perm'
    TYPE_PENDING = 'pend'
    TYPE_RESOLVED = 'solv'

    TYPE_NAMES = {
        TYPE_WARNING: 'Warning',
        TYPE_PERMITTED: 'Permitted',
        TYPE_PENDING: 'Pending',
        TYPE_RESOLVED: 'Resolved'
    }

    TYPE_CHOICES = (
        (TYPE_WARNING, TYPE_NAMES[TYPE_WARNING]),
        (TYPE_PERMITTED, TYPE_NAMES[TYPE_PERMITTED]),
        (TYPE_PENDING, TYPE_NAMES[TYPE_PENDING]),
        (TYPE_RESOLVED, TYPE_NAMES[TYPE_RESOLVED])
    )

    publication = models.OneToOneField('Publication',
                                       on_delete=models.CASCADE,
                                       primary_key=True,
                                       related_name='status')

    # warning, pending, resolved, permitted
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    description = models.CharField(max_length=300)
    solution = models.CharField(max_length=300, blank=True)


class Author(TimeStampedModel):
    """
    Represents an author of a research publication.
    """

    slug = models.SlugField(max_length=255, unique=True, editable=False, primary_key=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    scopus_id = models.CharField(max_length=100, blank=True, unique=True)

    publications = models.ManyToManyField('Publication',
                                          through='Authoring',
                                          blank=True,
                                          related_name='authors')

    institutions = models.ManyToManyField('Institution',
                                          through='Affiliation',
                                          blank=True,
                                          related_name="authors")

    meta_author = models.ForeignKey(
        'MetaAuthor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authors'
    )

    @property
    def full_name(self):
        """
        Returns the full name of the author as the first and last name separated by a whitespace

        :return:
        """
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name
        )

    def __str__(self):
        return self.full_name


class MetaAuthor(TimeStampedModel):
    """
    Represents a meta author.

    This model needs some further elaboration, as it is not as straight forward as the others. So the first question
    might be: How is a "MetaAuthor" different from the normal "Author" model?

    A normal author is simply simply a separate representation to store the information about who has worked on a
    publication. In some sense it simply extends the data type "publication". Publications are existent data they
    are gathered from some source and fed into this system, as such are the authors.
    A meta author is the representation of an author relevant to this very application. It is created for this
    application to represent an author, whose activities are supposed to be tracked/watched by the app. One meta
    author can also be connected to many normal author objects (that is mainly because there might be duplicate author
    profiles when importing from external sources). But in any way, creating a new meta author object on this site
    indicates that the publications of this author are of interest and are supposed to be tracked.

    THE INSTITUTION BLACKLIST
    So a meta author defines an author, whose publications are supposed to be tracked, because they are interesting
    to the purpose of the site. This purpose of the site is usually rather narrowly defined, such as tracking the
    activities of authors from a single institute or workgroup. Often authors have worked in different places and
    on different projects before. In such a case tracking all their activity might not be good, since all their
    previous work will also show up in the overview. Since external sources often provide the affiliated institution
    for an author of a publication it is possible to define a institution blacklist for a meta author to essentially
    say which of his previous work is uninteresting to the current purpose of the site.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # You can edit this, but if you leave it empty it will be generated automatically
    slug = models.SlugField(max_length=255,
                            unique=True,
                            primary_key=True)

    blacklisted_institutions = models.ManyToManyField('Institution',
                                                      through='Blacklisting',
                                                      blank=True,
                                                      null=True,
                                                      related_name='blacklisting_meta_authors')

    # The pof structure or "POF Struktur" is a KITOpen specific information. It defines to which project or rather
    # funding pool the publication belongs in the KIT internally.
    # It is possible to assign a default POF structure for an author. This will be assumed to belong to a publication
    # which he has worked on, in the case that the publication does not have that info yet.
    default_pof_structure = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return "{last}, {first}".format(
            last=self.last_name,
            first=self.first_name
        )

    @property
    def full_name(self):
        """
        Returns the full name of the author as the first and last name separated by a whitespace

        :return:
        """
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name
        )


# MANY-TO-MANY "THROUGH" MODELS


class Authoring(models.Model):
    """
    Represents a many to many link between an author and a publication. If an authoring object exists, that indicates
    that the given author has actively contributed to produce the given publication.
    """
    # Should this cascade?
    author = models.ForeignKey('Author', related_name='authorings', on_delete=models.SET_NULL, null=True)
    publication = models.ForeignKey('Publication', related_name='authorings', on_delete=models.SET_NULL, null=True)
    index = models.TimeField(auto_now=False, auto_now_add=True)


class Affiliation(models.Model):
    """
    Represents a many to many link between an author and an institution. If an affiliation object exists, that
    indicates that the given author is or has been affiliated with the given institution. In this case "being
    affiliated" with an institution means, that the author has worked in the name of this publication (using their
    funds) to produce some research.
    """
    author = models.ForeignKey('Author', related_name='affiliations', on_delete=models.SET_NULL, null=True)
    institution = models.ForeignKey('Institution', related_name='affiliations', on_delete=models.SET_NULL, null=True)


class Blacklisting(models.Model):
    """
    Represents a many to many link between a meta author and an institution. If a blacklisting object exists, that
    indicates that the given meta author blacklists the given institution. Specifically this means that all work that
    has been done by this author while working for this institution is supposed to be disregarded by the
    functionality of the pubs app, because it is not relevant to the current work of the author.
    """
    meta_author = models.ForeignKey('MetaAuthor', related_name='blacklistings', on_delete=models.SET_NULL, null=True)
    institution = models.ForeignKey('Institution', related_name='blacklistings', on_delete=models.SET_NULL, null=True)
