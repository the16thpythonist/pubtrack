"""
This module contains all the Serializers for this app's REST API

The objective of this app "pubs" is to provide a system for storing and accessing information about scientific
publications, their authors and other related data.

A "Serializer" is a class, which essentially defines the way how the conversion between the server internal
representation of data (i.e. the models) and the REST API data (request json content) is supposed to work.
"""
from rest_framework import serializers
from pubtrack.pubs.models import (Institution,
                                  Publication,
                                  PublicationStatus,
                                  Author,
                                  MetaAuthor,
                                  Authoring,
                                  Affiliation,
                                  Blacklisting)
from pubtrack.pubs.utils import (get_doi_url,
                                 get_kitopen_url,
                                 get_scopus_url)


class AuthorBriefField(serializers.RelatedField):
    """
    This is a custom implementation of RelatedField, which implements the display of Author data in a situation, where
    not the entire author object is supposed to be included

    DESIGN CHOICE
    So maybe some explanation for why this is important:
    Consider the model "Publication": If we request a publication, than we want one of the fields to be "authors",
    which is a list of all the Author objects, which are connected to this Publication object. This is being done by
    recursively invoking the AuthorSerializer for each author object of a publication.
    But now it would also be nice to get a full list "publications" whenever requesting and author. But in this case
    we could not just recursively call the PublicationSerializer, because that one already calls the AuthorSerializer.
    This would cause an infinite loop creating an infinitely nested structure to be returned for the request.
    Instead we define a special way to represent authors within a publications "authors" field, which only contain a
    limited amount of information, especially NOT referencing publications recursively!
    """

    def get_queryset(self):
        """
        Returns a queryset with all the "Author" objects.
        """
        return Author.objects.all()

    # value is the "AuthorProfile" object
    def to_representation(self, value) -> dict:
        """
        Returns the dict representation of the data to be inserted into the API response.

        In this case the author data includes the fields:
        - slug
        - first_name
        - last_name
        - scopus_id
        - meta_author           This is just the slug of the meta author and not the whole object

        :param value:
        :return:
        """
        obj = {
            'slug':             value.slug,
            'first_name':       value.first_name,
            'last_name':        value.last_name,
            'scopus_id':        value.scopus_id,
            'meta_author':      value.meta_author.slug if value.meta_author is not None else None
        }
        return obj


class InstitutionSerializer(serializers.ModelSerializer):
    """
    This class is the Serializer for the Institution model.

    For an API response an institution object is being represented by the following fields:
    - slug:                 str                 The slug of the object
    - modified:             datetime            When the object was modified the last time
    - name:                 str                 Name of the institution
    - city:                 str                 Location of the institution
    - scopus_id:            str                 Optional id of this institution within scopus database
    """

    class Meta:
        model = Institution
        fields = [
            # Read only
            'slug',
            'modified',
            # Editable - required
            'name',
            'city',
            # Editable - optional
            'scopus_id',
            # Related
            # 'authors',
            # 'blacklisting_meta_authors'
        ]


class PublicationStatusSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PublicationStatus
        fields = [
            # read-only
            'modified',
            # editable - required
            'publication',
            'type',
            'description',
            # editable - optional
            'solution',
            # computed
            'name'
        ]

    def get_name(self, obj):
        return PublicationStatus.TYPE_NAMES[obj.type]


class PublicationSerializer(serializers.ModelSerializer):
    """
    This class is the Serializer for the Publication Model

    For an API response of a publication object, the following fields are given:
    - uuid:                 str                 Unique id of the publication within this database
    - modified:             datetime            When the object was last modified
    - title:                str                 Title of the publication
    - published:            datetime            When the publication was published within the journal etc.
    - scopus_id             str                 Optional id of the publication within scopus database
    - on_kitopen            bool                Whether the publication was fount on KITOpen database
    - kitopen_id            str                 Optional id of the publication within KITOpen
    - pof_structure         str                 Optional str repr. of the "POF Struktur" within KITOpen
                                                This is an identifier for the project funds used for this pub.
    - authors               list                List of all author objects for this publication as returned by
                                                AuthorSerializer
    - meta_authors          list                List of shortened representations for the meta authors, which were
                                                involved in this publication. This is a computed property, which just
                                                iterates all the authors and extracts the meta authors from them
    """

    authors = AuthorBriefField(
        many=True,
        allow_empty=True,
        read_only=True
    )

    meta_authors = serializers.SerializerMethodField()
    status = PublicationStatusSerializer(read_only=True)

    doi_url = serializers.SerializerMethodField(read_only=True)
    scopus_url = serializers.SerializerMethodField(read_only=True)
    kitopen_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Publication
        fields = [
            # Read only
            'uuid',
            'modified',
            # Editable - required
            'title',
            'published',
            # Editable - optional
            'scopus_id',
            'scopus_url',
            'on_kitopen',
            'kitopen_id',
            'kitopen_url',
            'doi',
            'doi_url',
            'pof_structure',
            # Related
            'authors',
            'status',
            # Computed
            'meta_authors'
        ]

    def get_meta_authors(self, obj):
        """
        Returns a list of dicts, which contain brief information about the meta authors involved with this publication

        DESIGN CHOICE
        So why do we need this field? The frontend application at some points needs a list of all involved meta authors
        for a publication. Of course its a calculation, which could be done in the frontend too, but caching it and
        making it efficient is more of a hassle than just doing it here.

        The meta author dicts contain the following keys:
        - slug              str                 The unique slug of the author
        - full_name         str                 The first and last name of the author separated by white space
        :param obj:
        :return:
        """
        # So this is strange: We are using a dict to store all the meta author informations only to return just the
        # values anyways... Could we not just use a list.
        # Well no, because this is a more efficient way of avoiding duplicates. By using a unique key for the dict,
        # there will be no duplicate entries. This is more efficient then constructing a list and removing the
        # duplicates afterwards!
        meta_authors = {}
        for author in obj.authors.all():
            if author and author.meta_author:
                meta_authors[author.meta_author.slug] = {
                    'slug':         author.meta_author.slug,
                    'full_name':    author.meta_author.full_name
                }
        return meta_authors.values()

    def get_doi_url(self, obj):
        return get_doi_url(obj.doi) if obj.doi else ''

    def get_scopus_url(self, obj):
        return get_scopus_url(obj.scopus_id) if obj.scopus_id else ''

    def get_kitopen_url(self, obj):
        return get_kitopen_url(obj.kitopen_id) if obj.kitopen_id else ''


class MetaAuthorBriefField(serializers.RelatedField):
    """
    This is a custom implementation of RelatedField, which implements the display of MetaAuthor data in a situation,
    where not the entire object is supposed to be included.

    This stripped down representation of the meta author includes:
    - slug                  str                 Unique slug of the meta author
    - first_name            str                 First name of the meta author
    - last_name             str                 Last name of the meta author
    """

    def get_queryset(self):
        """
        Returns the queryset for all the MetaAuthor objects

        :return:
        """
        return MetaAuthor.objects.all()

    def to_representation(self, value):
        """
        Returns the dict representation of the data to be inserted into the API response.

        This is a method from the abstract "RelatedField", which has to be overwritten

        :param value:
        :return:
        """
        if value is None:
            obj = {'slug': None}
        else:
            obj = {
                'slug':         value.slug,
                'first_name':   value.first_name,
                'last_name':    value.last_name
            }
        return obj

    def to_internal_value(self, data):
        """
        This method takes the data from a request in dict format and has to return and internal object representation
        of a model.

        This is a method from the abstract "RelatedField", which has to be overwritten in case these custom
        representations of meta authors are also supposed to be supported for POST operations.

        :param data:
        :return:
        """
        # Of course we are simply trying to find if an author with the given slug exists and then return that
        meta_authors = MetaAuthor.objects.filter(slug__exact=data['slug'])
        if meta_authors.exists():
            return meta_authors.first()
        else:
            raise serializers.ValidationError("The given slug does not belong to any meta author!")


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model

    For an API response of a meta author object, the following fields are given:
    - slug                  str                 The unique slug of an object
    - first_name            str                 First name of author
    - last_name             str                 Last name of author
    - scopus_id             str                 Optional id of author within scopus database
    - publications          list                List of author objects, which have authored this publication as
                                                returned by PublicationSerializer
    - meta_author           str                 Optional slug of the meta author, which this profile is ass. to
    """
    publications = PublicationSerializer(many=True, allow_null=True, read_only=True)
    institutions = InstitutionSerializer(many=True, allow_null=True, read_only=True)
    meta_author = MetaAuthorBriefField(allow_null=True, allow_empty=True, required=False)

    class Meta:
        model = Author
        fields = [
            # This is read only
            'slug',
            # These are the only fields that can be used for POST
            'first_name',
            'last_name',
            'scopus_id',
            # Related models
            'publications',
            'institutions',
            'meta_author'
        ]


class MetaAuthorSerializer(serializers.ModelSerializer):
    """
    The Serializer for the MetaAuthor model

    Quick reminder: A MetaAuthor in contrast to just Author is the information of an author specifically
    observed by the application. A MetaAuthor is a top level representation of an author, which also may or may not be
    represented by multiple Author profiles.

    For an API response of a meta author object, the following fields are given:
    - created:              datetime            When the object was created
    - first_name:           str                 First name of the author
    - last_name:            str                 Last name of the author
    - slug:                 str                 Unique slug of the author
    - authors:              list                List of all author objects associated with the meta author as returned
                                                by AuthorSerializer
    - blacklisted_institutions                  List of all the institutions blacklisted for this meta author as
                                                returned by InstitutionSerializer
    """
    # You may not wanna render all the details of those here. This is for the moment
    # but it could be replaced by computed fields which simply give the scopus ids and the
    # ids of the blacklisted affiliations
    authors = AuthorSerializer(many=True, allow_null=True, read_only=True)
    blacklisted_institutions = InstitutionSerializer(many=True, allow_null=True, read_only=True)

    class Meta:
        model = MetaAuthor
        fields = [
            # Read only
            'created',
            # Editable - required
            'first_name',
            'last_name',
            'slug',
            # Editable - optional
            # --
            # Related
            'authors',
            'blacklisted_institutions'
        ]


class AuthoringSerializer(serializers.ModelSerializer):
    """
    Serializer for the Authoring model

    An authoring is an intermediate object, which describes the many to many connection between an author and a
    publication. it consists of the respective primary keys thus describing that a given author has worked on the
    given publication.

    For an API response of a meta author object, the following fields are given:
    - author:               str                 The slug of the author (primary key)
    - publication:          str                 The uuid of the publication (primary key)
    """
    class Meta:
        model = Authoring
        fields = [
            'author',
            'publication'
        ]


class AffiliationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Affiliation model

    An affiliation is an intermediate object, which describes the many to many connection between an author and a
    institution. An affiliation describes that the given author is affiliated with the given institution

    For an API response of a meta author object, the following fields are given:
    - author:               str                 The slug of the author (primary key)
    - institution           str                 The slug of the institution (primary key)
    """
    class Meta:
        model = Affiliation
        fields = [
            'author',
            'institution'
        ]


class BlacklistingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blacklisting model

    A blacklisting is an intermediate object, which describes the many to many relationship between a meta author and a
    institution. A blacklisting describes that the given institution is blacklisted for the given meta author.

    For an API response of a meta author object, the following fields are given:
    - meta_author           str                 The slug of the meta author (primary key)
    - institution           str                 The slug of the institution (primary key)
    """
    class Meta:
        model = Blacklisting
        fields = [
            'meta_author',
            'institution'
        ]
