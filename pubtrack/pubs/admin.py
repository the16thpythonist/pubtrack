import os
from django.contrib import admin
from pubtrack.pubs.models import (Institution,
                                  Publication,
                                  Author,
                                  MetaAuthor)


class AuthorAdminInline(admin.TabularInline):
    model = Author


class MetaAuthorAdmin(admin.ModelAdmin):

    inlines = (AuthorAdminInline, )


if 'DOC' not in os.environ.keys():
    admin.site.register(Institution)
    admin.site.register(MetaAuthor, MetaAuthorAdmin)
    admin.site.register(Author)
    admin.site.register(Publication)
