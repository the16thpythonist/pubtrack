
from django.conf import settings
from pubtrack.pubs.models import PublicationStatus, Publication


def create_publication_status(publication):
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
