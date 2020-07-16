from typing import Dict, Union
import datetime

from django.conf import settings
from pubtrack.pubs.models import PublicationStatus, Publication


def create_publication_status(publication: Publication):
    kwargs = {
        'publication':              publication,
        'type':                     PublicationStatus.TYPE_RESOLVED,
        'description':              'there is no problem!'
    }

    if not publication.on_kitopen:
        kwargs.update({
            'type':                 PublicationStatus.TYPE_WARNING,
            'description':          'Publication is not on KITOpen'
        })

    elif publication.pof_structure not in settings.PUBS_CONFIG['accepted_pofs']:
        kwargs.update({
            'type':                 PublicationStatus.TYPE_WARNING,
            'description':          'Wrong POF Structure'
        })

    return PublicationStatus.objects.create(**kwargs)


def update_publication_status(publication: Publication):

    # So the way this should work is that if the publication status is in pending or permitted then the only
    # allowed change is towards the resolved state.
    # If the status of the publication is resolved then we dont need to do anything anyways and if the status of the
    # publication is warning, every change is allowed

    updater = PublicationStatusUpdater(publication)
    return updater.update()


class PublicationStatusUpdater:

    def __init__(self, publication: Publication):
        self.publication = publication

        self.status_qs = PublicationStatus.objects.filter(publication=publication)
        self.status = self.status_qs.first()

        self.kwargs = self.get_issue()
        self.kwargs = self.add_solution(self.kwargs)

    # PUBLIC METHODS
    # --------------

    def update(self):

        if self.is_status_pending() or self.is_status_permitted():
            if self.kwargs['type'] == PublicationStatus.TYPE_RESOLVED:
                self.status_qs.update(**self.kwargs)

        if self.is_status_warning():
            self.status_qs.update(**self.kwargs)

        return self.status_qs.first()

    def is_status_resolved(self):
        return self.status.type == PublicationStatus.TYPE_RESOLVED

    def is_status_permitted(self):
        return self.status.type == PublicationStatus.TYPE_PERMITTED

    def is_status_warning(self):
        return self.status.type == PublicationStatus.TYPE_WARNING

    def is_status_pending(self):
        return self.status.type == PublicationStatus.TYPE_PENDING

    def get_issue(self):
        kwargs = {
            'type':             PublicationStatus.TYPE_RESOLVED,
            'description':      'there is no problem!'
        }

        if not self.publication.on_kitopen:
            kwargs.update({
                'type':         PublicationStatus.TYPE_WARNING,
                'description':  'Publication not on KITOpen'
            })

        print(self.publication.pof_structure)
        print(settings.PUBS_CONFIG)
        if self.publication.pof_structure not in settings.PUBS_CONFIG['accepted_pofs']:
            kwargs.update({
                'type':         PublicationStatus.TYPE_WARNING,
                'description':  'Wrong POF structure!'
            })

        return kwargs

    def add_solution(self, kwargs):
        if kwargs['type'] == PublicationStatus.TYPE_RESOLVED and not self.is_status_resolved():
            solution_template = '[{}] Automatic Status Update: {}({}) >> {}'
            solution = solution_template.format(
                str(datetime.datetime.now().date()),
                self.status.type,
                self.status.description,
                PublicationStatus.TYPE_NAMES[kwargs['type']].upper()
            )
            kwargs['solution'] = solution

        return kwargs