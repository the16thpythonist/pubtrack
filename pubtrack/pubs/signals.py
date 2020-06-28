from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

from pubtrack.pubs.utils import generate_random_string
from pubtrack.pubs.models import (Institution,
                                  Publication,
                                  PublicationStatus,
                                  Author,
                                  MetaAuthor)
from pubtrack.pubs.status import create_publication_status, update_publication_status

# SLUG GENERATION

"""
THE REASONING FOR THE SLUGS

Why not use standard, incremental primary keys for the models?
It is actually highly discouraged to use incremental primary keys for a (more or less) public REST Api, because 
through the incremental nature an outside perspective can gain knowledge about the structure of the internal 
database, which is a security risk.

Why not use UUID's for everything?
The first alternative to a incremental key would be a uuid, but I did not want to use these due to my personal 
preference. A uuid is just a random key, there is no kind of information stored about the actual object, which it 
represents. This is why a slug is better. It is a string, which can contain some sort of informational value.
So I am using slugs as the primary key for a lot of the models. But at the same time I also set this slug to read only, 
which means that the user cannot edit it. Having a slug as the primary field and have it be editable by the user 1) 
has a certain risk, because the user might not know which slugs are already given or not incorporate the information 
into it consistently and 2) Might also be huger inconvenience for the user to have to come up with a unique slug every 
time a new object is to be created.
So the obvious alternative is to create a slug for the objects automatically, which has the advantage, that for every 
object it contains the exact same information consistently.
An issue with creating slugs automatically of course is that not all the other fields, from which the slug is created 
are unique fields. That creates the possibility that there could be duplicates. That is why every slug is also appended 
with a 4 letter random string, which reduces the possibilities for duplicates to practically zero.
Using this technique the primary key of an object at least gives some sort of a hint towards the content of the object, 
which is better than just a random key in my opinion.
"""

# Note, that these have to be pre-save, since the slug has to exist for the object being able to be inserted into
# the database


@receiver(pre_save, sender=Author)
def add_slug_to_author_profile(sender, instance, *args, **kwargs):
    """
    Adds a slug to an AuthorProfile object, when it is first being saved

    The slug has the following format
    {First name of author}-{Last name of author}-{Random 4 letter string}

    :param sender:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    if instance and not instance.slug:
        slugified_first_name = slugify(instance.first_name)
        slugified_last_name = slugify(instance.last_name)
        random_string = generate_random_string(length=4)
        instance.slug = "{first}-{last}-{rnd}".format(
            first=slugified_first_name,
            last=slugified_last_name,
            rnd=random_string
        )


@receiver(pre_save, sender=Institution)
def add_slug_to_affiliation(sender, instance, *args, **kwargs):
    """
    Adds a slug to an Institution object, when it is first being saved.

    The slug has the following format:
    {Name of the institution}-{City, where it is located}-{Random 4 letter string}

    :param sender:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    if instance and not instance.slug:
        slugified_name = slugify(instance.name)
        slugified_city = slugify(instance.city)
        random_string = generate_random_string(length=4)
        instance.slug = '{name}-{city}-{rnd}'.format(
            name=slugified_name,
            city=slugified_city,
            rnd=random_string
        )


# This has to be post-save, because a PublicationStatus object can only be created with a reference to a valid
# primary key of an existing Publication object


@receiver(post_save, sender=Publication)
def add_status_to_publication(sender, instance, *args, **kwargs):
    """
    For every Publication that is being saved, a PublicationStatus will be created and associated with it.

    BACKGROUND
    A PublicationStatus object contains information, which is not inherent to the publication (external), but which is
    only really relevant to the "pubs" app and its functionality itself (internal). A publication status will provide
    information about whether or not there is a problem with a publication which has to be addressed.

    A status can be computed from the properties of a Publication object and that is exactly what is being done here.
    Based on the state of the Publication and according status object will be created and associated with the
    publication object as a one to one relation between the models.

    As a matter of fact, a status cannot even be provided when creating a new object, since the whole point of the
    status is more or less, that it can be automatically derived. It is possible however that the user makes a
    custom modification to the status once the publication object already exists.

    :param sender:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    if instance:
        qs = PublicationStatus.objects.filter(publication=instance)
        if not qs.exists():
            # "create_publication_status" is the function, which actually computes the status, based on the state of
            # the publication. The logic, or the reasoning, what publication details result in which status can be
            # found there.
            # It already inserts the status object into the database and returns that object
            obj = create_publication_status(instance)
            print("Added a new PublicationStatus", obj)
        else:
            # In this case it has to be updated...
            obj = update_publication_status(instance)
