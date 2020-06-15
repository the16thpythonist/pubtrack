from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings

from pubtrack.pubs.mixins import MultipleFieldLookupMixin, NestedFieldLookupMixin, ThroughModelLookupMixin
from pubtrack.pubs.models import (Institution,
                                  Publication,
                                  PublicationStatus,
                                  Author,
                                  MetaAuthor,
                                  Authoring,
                                  Affiliation,
                                  Blacklisting)
from pubtrack.pubs.api.serializers import (InstitutionSerializer,
                                           PublicationSerializer,
                                           PublicationStatusSerializer,
                                           AuthorSerializer,
                                           MetaAuthorSerializer,
                                           AuthoringSerializer,
                                           AffiliationSerializer,
                                           BlacklistingSerializer)


class AuthorListCreateAPIView(generics.ListCreateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'scopus_id']


class AuthorRUDAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'slug'


class MetaAuthorListCreateAPIView(generics.ListCreateAPIView):

    queryset = MetaAuthor.objects.all()
    serializer_class = MetaAuthorSerializer
    permission_classes = [IsAuthenticated]


class MetaAuthorRUDAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = MetaAuthor.objects.all()
    serializer_class = MetaAuthorSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'slug'


class PublicationListCreateAPIView(generics.ListCreateAPIView):

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scopus_id']


class PublicationRUDAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'uuid'


class PublicationStatusListCreateAPIView(generics.ListCreateAPIView):

    queryset = PublicationStatus.objects.all()
    serializer_class = PublicationStatusSerializer
    permission_classes = [IsAuthenticated]


class PublicationStatusRUDAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = PublicationStatus.objects.all()
    serializer_class = PublicationStatusSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'publication'


class AuthoringListCreateAPIVIew(generics.ListCreateAPIView):

    queryset = Authoring.objects.all()
    serializer_class = AuthoringSerializer
    permission_classes = [IsAuthenticated]


class AuthoringRUDAPIView(ThroughModelLookupMixin,
                          generics.RetrieveUpdateDestroyAPIView):

    queryset = Authoring.objects.all()
    serializer_class = AuthoringSerializer
    permission_classes = [IsAuthenticated]

    lookup_fields = [
        {
            'kwarg':            'author_slug',
            'class':            Author,
            'related_name':     'author',
            'related_field':    'slug'
        },
        {
            'kwarg':            'publication_uuid',
            'class':            Publication,
            'related_name':     'publication',
            'related_field':    'uuid'
        }
    ]


class InstitutionListCreateAPIView(generics.ListCreateAPIView):

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]


class InstitutionRUDAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'slug'


class AffiliationListCreateAPIView(generics.ListCreateAPIView):

    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    permission_classes = [IsAuthenticated]


class AffiliationRUDAPIView(ThroughModelLookupMixin,
                            generics.RetrieveUpdateDestroyAPIView):
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    permission_classes = [IsAuthenticated]

    lookup_fields = [
        {
            'kwarg': 'author_slug',
            'class': Author,
            'related_name': 'author',
            'related_field': 'slug'
        },
        {
            'kwarg': 'institution_slug',
            'class': Institution,
            'related_name': 'institution',
            'related_field': 'slug'
        }
    ]


class BlacklistingListCreateAPIView(generics.ListCreateAPIView):

    queryset = Blacklisting.objects.all()
    serializer_class = BlacklistingSerializer
    permission_classes = [IsAuthenticated]


class BlacklistingRUDAPIView(ThroughModelLookupMixin,
                             generics.RetrieveUpdateDestroyAPIView):

    queryset = Blacklisting.objects.all()
    serializer_class = BlacklistingSerializer
    permission_classes = [IsAuthenticated]

    lookup_fields = [
        {
            'kwarg': 'meta_author_slug',
            'class': MetaAuthor,
            'related_name': 'meta_author',
            'related_field': 'slug'
        },
        {
            'kwarg': 'institution_slug',
            'class': Institution,
            'related_name': 'institution',
            'related_field': 'slug'
        }
    ]


class ConfigAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(settings.PUBS_CONFIG)
