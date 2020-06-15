from django.urls import include, path

from rest_framework.routers import DefaultRouter

from pubtrack.pubs.api.views import (AuthorListCreateAPIView,
                                     AuthorRUDAPIView,
                                     MetaAuthorListCreateAPIView,
                                     MetaAuthorRUDAPIView,
                                     PublicationListCreateAPIView,
                                     PublicationRUDAPIView,
                                     PublicationStatusListCreateAPIView,
                                     PublicationStatusRUDAPIView,
                                     InstitutionListCreateAPIView,
                                     InstitutionRUDAPIView,
                                     AuthoringListCreateAPIVIew,
                                     AuthoringRUDAPIView,
                                     AffiliationListCreateAPIView,
                                     AffiliationRUDAPIView,
                                     BlacklistingListCreateAPIView,
                                     BlacklistingRUDAPIView,
                                     ConfigAPIView)


router = DefaultRouter()


urlpatterns = [
    # AUTHORS
    # -------
    # /authors/                                                             GET POST
    path("authors/",
         AuthorListCreateAPIView.as_view(),
         name="authors-list"),

    # /authors/:slug                                                        GET PUT DELETE
    path("authors/<slug:slug>/",
         AuthorRUDAPIView.as_view(),
         name="authors-detail"),

    # PUBLICATION
    # -----------
    # /publications/                                                        GET POST
    path("publications/",
         PublicationListCreateAPIView.as_view(),
         name="publications-list"),

    # /publications/:uuid/                                                  GET PUT DELETE
    path("publications/<uuid:uuid>/",
         PublicationRUDAPIView.as_view(),
         name="publications-detail"),

    # PUBLICATION STATUS
    # ------------------
    # /publication-statuses/
    path("publication-statuses/",
         PublicationStatusListCreateAPIView.as_view(),
         name="publication-statuses-list"),

    # /publication-statuses/:publication_uuid/
    path("publication-statuses/<uuid:publication>/",
         PublicationStatusRUDAPIView.as_view(),
         name="publication-statuses-detail"),

    # INSTITUTIONS
    # ------------
    # /institutions/                                                       GET POST
    path("institutions/",
         InstitutionListCreateAPIView.as_view(),
         name="institutions-list"),

    # /institutions/:slug/                                                  GET PUT DELETE
    path("institutions/<slug:slug>",
         InstitutionRUDAPIView.as_view(),
         name="institutions-detail"),

    # META AUTHORS
    # ------------
    # /meta_authors/                                                        GET POST
    path("meta-authors/",
         MetaAuthorListCreateAPIView.as_view(),
         name="meta-authors-list"),

    # /meta_authors/:slug/                                                  GET PUT DELETE
    path("meta-authors/<slug:slug>/",
         MetaAuthorRUDAPIView.as_view(),
         name="meta-authors-list"),

    # AUTHORINGS
    # ----------
    # /authorings/                                                          GET POST
    path("authorings/",
         AuthoringListCreateAPIVIew.as_view(),
         name="authorings-list"),

    # /authorings/:author_slug/:publication_uuid/                           GET PUT DELETE
    path("authorings/<slug:author_slug>/<uuid:publication_uuid>/",
         AuthoringRUDAPIView.as_view(),
         name="authorings-detail"),

    # AFFILIATIONS
    # ------------
    # /affiliations/                                                        GET POST
    path("affiliations/",
         AffiliationListCreateAPIView.as_view(),
         name="affiliations-list"),

    # /affiliations/:author_slug/:institution_slug/                         GET PUT DELETE
    path("affiliations/<slug:author_slug>/<slug:institution_slug>/",
         AffiliationRUDAPIView.as_view(),
         name="affiliations-detail"),

    # BLACKLISTINGS
    # -------------
    # /blacklistings/                                                       GET POST
    path("blacklistings/",
         BlacklistingListCreateAPIView.as_view(),
         name="blacklistings-list"),

    # /blacklistings/:meta_author_slug/:institution_slug                    GET PUT DELETE
    path("blacklistings/<slug:meta_author_slug>/<slug:institution_slug>/",
         BlacklistingRUDAPIView.as_view(),
         name="blacklistings-detail"),

    # CONFIG
    path("config/",
         ConfigAPIView.as_view(),
         name="config")
]
