"""
This module contains all the Models for this app.

The objective of this app "pubs" is to provide a system for storing and accessing information about scientific
publications, their authors and other related data.

The models define the structure of the data, which is supposed to be managed by the app. Each model more or less
represents an object, which has multiple properties and methods. These objects will be persistently saved into the
sites database and can be queried to provide some sort of information to the REST interface and thus the frontend
user.
"""
import os

from django.db import models
import uuid

from model_utils.models import TimeStampedModel


"""
**A note on primary keys**

So by inspecting the implementations within this module, one could see that the primary keys for most of the models 
are realized as slugs. These slugs can either be edited by the user or are automatically created from other textual 
properties of the models. This has a reason: Slugs provide some sort of readability and meaning for the human user in 
contrary to numerical id's for example.

But there is an exception: The publication model uses a uuid as a primary field, which obviously has no kind of meaning 
for a human. This has the following reasons:
- A slug for a user would have to be created from the title. With scientific publications possibly having very long 
titles I felt like thay might be *too* long for a primary key (which then would also be used as a url part for the REST
API...)
- Also some very mathematical publications might have special character in the title, which would have to be removed 
for a slug. And the title might loose its meaning without those characters in it.

Now a question would be "Why go for a uuid, if you could just use a simple auto incrementing index?". Well, actually 
using a numeric index is bad practice, because it obviously provided some sort of insight about the structure of the 
internal sql table and that is a potential security issue, especially if the models are supposed to be exposed by a 
web API! So the better solution in the case of not using a slug is to always use a uuid!

**A note on the slug fields**

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

    **Details**

    An institution object represents some kind of a research facility. First of: Why is this information even important.
    When other databases such as Scopus save information about a publication, they also save data about the authors of
    the publication and with these authors also the institute, which they are affiliated with. Now in the real world it
    is the case that authors sometimes change jobs and thus switch the facilities they are affiliated with it could be
    that an author has published *for* different institutes in the whole of his career. Now the pubs application works
    by maintaining a set of observed authors and frequently pulling the information about all of their publications.
    The use case of the application being to track all the publications for a specific workgroup or institute. This
    implies that the information about the affiliated institute is needed to potentially filter out those publications
    which an author has published for a different institute, which is not the one actually employing the pubs
    application!
    """

    # TODO: Write a comment about this!
    class Meta:
        app_label = 'pubs'


    slug = models.SlugField(max_length=255, unique=True, editable=False, primary_key=True)
    """
    :ivar slug: kek
    """

    scopus_id = models.CharField(max_length=80, unique=True, blank=True)
    """
    :ivar scopus_id:
    """

    name = models.CharField(max_length=255)
    """
    :ivar name:
    """

    city = models.CharField(max_length=255)
    """
    :ivar city:
    """

    def __str__(self) -> str:
        """
        Returns the string representation of an institution.

        :return:
        """
        return "Institution(name='{name}', city='{city}', scopus_id='{scopus_id}')".format(
            name=self.name,
            city=self.city,
            scopus_id=self.scopus_id
        )


class Publication(TimeStampedModel):
    """
    Represents a research publication.

    **Details**

    The publication model is the main model for the pubs app. The whole functionality basically revolves around managing
    these publications. The real world equivalent to this model are the various scientific documents the scientists
    write and then publish in journals or conferences. These publications are also the subject of various other
    databases like Scopus and KITOpen. What the pubs application essentially only does is to import the knowledge about
    these publications from these other databases and "mirror" them into the local model.

    :ivar uuid: This field contains a uuid for the publication. This uuid is generated automatically for each
               publication and acts as the primary key for the model. The uuid is generated randomly and does not
               contain any sort of information about the publication.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    """
    :ivar uuid: This field contains a uuid for the publication. This uuid is generated automatically for each 
               publication and acts as the primary key for the model. The uuid is generated randomly and does not 
               contain any sort of information about the publication.
    """

    """
    :ivar title: This field contains the string title of the publication.
    """
    title = models.CharField(max_length=255)

    """
    :ivar published: This is a datetime field, which contains the date and time at which this publication was originally 
                    published in a journal etc.
    """
    published = models.DateTimeField(null=True)

    """
    :ivar doi: This field contains the string DOI (digitial object identifier) of the publication. It may be empty if 
              that info could not be extracted from the source data.
    """
    doi = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # SCOPUS RELATED FIELDS
    # ---------------------
    """
    :ivar scopus_id: This field contains the string version of the scopus id for the publication. The scopus id is the 
                    primary key of the publication within the scopus database and the main way publication is identified 
                    for scopus.
    """
    scopus_id = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # 19.06.2020: So apparently you need the eid of a publication to access the scopus detail page of that publication
    """
    :ivar eid: This field contains the eid of a publication.
    """
    eid = models.CharField(max_length=80, blank=True, null=True, unique=True)

    # KITOPEN RELATED FIELDS
    # -----------------------

    """
    :ivar on_kitopen: This is a boolean flag, which contains the information of whether or not the publication has been 
                     found within the KITOpen database. In retrospect, this field is redundant because with the kitopen 
                     ID field being able to be blank, I could have simply made this a computed property.
    """
    on_kitopen = models.BooleanField(default=False)

    """
    :ivar kitopen_id: This field contains the string representation of the KITOpen ID for the publication. The field can 
                     be empty, if the publication is not yet found in the KITOpen database.
    """
    kitopen_id = models.CharField(max_length=80, blank=True, null=True, unique=True)

    """
    :ivar pof_structure: This field contains the string representation of the POF structure of a publication. But what 
                        even is a 'pof structure'? Essentially it is a kind of ID string, which is an important 
                        property of a publication within the KITOpen database. The pof string contains information 
                        about how a publication was funded internally at the KIT. Arguably this could be the single 
                        most important property for this application, because the assignment to a certain pof is 
                        detrimental for the generation of metrics for the performance evaluation of an institute.
    """
    pof_structure = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self) -> str:
        """
        Returns the string representation of a publication.

        :return:
        """
        return "Publication(title='{title}', published='{published}', doi='{doi}', 'kitopen_id='{kitopen_id}')".format(
            title=self.title,
            published=self.published,
            doi=self.doi,
            kitopen_id=self.kitopen_id
        )


class PublicationStatus(TimeStampedModel):
    """
    Represents the current status of a publication.

    **Details**

    To manage the status of a publication is kind of the whole purpose of the pubtrack project. First of lets answer
    the question "status in regards to what?". The important status here refers to whether or not the publication is
    correctly inserted into the KITOpen database. There are 4 possible statuses, which a publication can take on:
    - warning: This is the status when the pubtrack system has detected an error with the publication within KITOpen
    - solved: With this status all problems have been resolved and all the properties of the publication in regards to
      the KITOpen database are exactly as they are supposed to be.
    - pending: This status is given to a publication when a process to solve the issues has been initiated, but has not
      yet terminated. (This could be the case if another person will solve the problem sometime in the future for ex.)
    - permitted: This status can be assigned to a publication, which has issues to mark these problems as not needed to
      be solved. This is important if the pubtrack system for example missclassifies a publication.
    """

    # NOTE about the following section:
    # This way of defining choices for a char field, that is using class variables for the identifiers and then a
    # separate class constant to define the actual choices is the recommended way to do it by the book "two scoops of
    # django"
    TYPE_WARNING = 'warn'
    TYPE_PERMITTED = 'perm'
    TYPE_PENDING = 'pend'
    TYPE_RESOLVED = 'solv'

    """
    :cvar TYPE_NAMES: This is a class constant, which is a dict whose keys are the string ID's of the status type and 
                      the values are human readable names for those statuses. This dict is used to display the status 
                      to the user, whereas the actual ID's are used more for internal processes.
    """
    TYPE_NAMES = {
        TYPE_WARNING: 'Warning',
        TYPE_PERMITTED: 'Permitted',
        TYPE_PENDING: 'Pending',
        TYPE_RESOLVED: 'Resolved'
    }

    """
    :cvar TYPE_CHOICES: This is a class constant, which defines a tuple for the choices to be passed to the django 
                        CharField.
    """
    TYPE_CHOICES = (
        (TYPE_WARNING, TYPE_NAMES[TYPE_WARNING]),
        (TYPE_PERMITTED, TYPE_NAMES[TYPE_PERMITTED]),
        (TYPE_PENDING, TYPE_NAMES[TYPE_PENDING]),
        (TYPE_RESOLVED, TYPE_NAMES[TYPE_RESOLVED])
    )

    """
    :ivar publication: This is a one to one relationship with the publication model. Obviously every publication is 
                      assigned exactly one status and vice versa. This acts as the primary key for the status model.
    """
    publication = models.OneToOneField('Publication',
                                       on_delete=models.CASCADE,
                                       primary_key=True,
                                       related_name='status')

    """
    :ivar type: This field saves the string representation of the *kind of* status this actually is. This field can only 
               take on a discrete set of choices (4 to be specific). These are solv, perm, pend, warn.
    """
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)

    """
    :ivar description: Every status is additionally assigned a description. This description is supposed to contain a 
                      human readable string of an explanation of the exact problem, which the publication has. 
                      This string is either set automatically by the pubtrack system, when it detects an issue. It can 
                      however also be manually written by the user.
    """
    description = models.CharField(max_length=300)

    """
    :ivar solution: Additionally every status has a solution string. This is supposed to contain a human readable 
                   explanation of what steps have resulted in the resolving of the publications issues. This also can 
                   be automatically generated or manually written by the user
    """
    solution = models.CharField(max_length=300, blank=True)


class Author(TimeStampedModel):
    """
    Represents an author of a research publication.

    **Details**

    Now there is an important detail about the author model: This model is not a one to one mapping towards a real
    person. Specifically a real person may have multiple author objects describing them. This has a very practical
    reason: These author profiles are fetched from the scopus database and this database also sometimes has duplicate
    profiles, because authors a differently written in some publications which sparks the creation of a new profile.
    """

    """
    :ivar first_name: Each author has a first/given name. NOTE: since this field is often filled in automatically with 
                     the data from the scopus database for example, it may not contain the full first name, but just 
                     the first latter and a period, because that is a common way to give the name in a scientific 
                     publication.
    """
    first_name = models.CharField(max_length=100)

    """
    :ivar last_name: Each author has a last/family name.
    """
    last_name = models.CharField(max_length=100)

    """
    :ivar slug: Each author is identified by slug, which acts as the primary key of the model. This slug is not editable 
               by the user. It will be generated automatically from the first and last name of the author once a new 
               author is being saved. This generation of the slug is implemented as a pre save signal.
    """
    slug = models.SlugField(max_length=255, unique=True, editable=False, primary_key=True)

    """
    :ivar scopus_id: This field saves the scopus ID for every author. The scopus ID is essentially the primary key of 
                    an author within the scopus database, thus it has to be unique. It can however also be blank. An 
                    author does not have to have a scopus id.
    """
    scopus_id = models.CharField(max_length=100, blank=True, unique=True)

    """
    :ivar publications: This field is the many to many relation with the publication model. It saves reference of all 
                       publications, which the author has worked on in the past. See the Authoring model for the 
                       details.
    """
    publications = models.ManyToManyField('Publication',
                                          through='Authoring',
                                          blank=True,
                                          related_name='authors')

    """
    :ivar institutions: This field is the many to many relation with the institutions model. It describes all the 
                       institutions an author has been affiliated with in his career. See the Affiliation model for 
                       the details.
    """
    institutions = models.ManyToManyField('Institution',
                                          through='Affiliation',
                                          blank=True,
                                          related_name="authors")

    """
    :ivar meta_author: This field describes the many to one relationship with the meta author. Since the author model 
                      is allowed for duplicate entries which in theory describe the same person, the meta author model 
                      is the attempt to describe all these duplicates by a single model again. A meta author object 
                      is unique for every person, but it can be related to many author objects.
    """
    meta_author = models.ForeignKey('MetaAuthor',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name='authors')

    def __str__(self):
        """
        Returns the string representation of an author.

        **Example**

        The string representation of an author looks like the following format
        "Author(slug='{slug}', full_name='{full_name}', scopus_id='{scopus_id}')"

        :return:
        """
        return "Author(slug='{slug}', full_name='{full_name}', scopus_id='{scopus_id}')".format(
            slug=self.slug,
            full_name=self.full_name,
            scopus_id=self.scopus_id
        )

    # UTILITY METHODS
    # ---------------

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


class MetaAuthor(TimeStampedModel):
    """
    Represents a meta author.

    **Details**

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

    **The Institution Blacklist**

    So a meta author defines an author, whose publications are supposed to be tracked, because they are interesting
    to the purpose of the site. This purpose of the site is usually rather narrowly defined, such as tracking the
    activities of authors from a single institute or workgroup. Often authors have worked in different places and
    on different projects before. In such a case tracking all their activity might not be good, since all their
    previous work will also show up in the overview. Since external sources often provide the affiliated institution
    for an author of a publication it is possible to define a institution blacklist for a meta author to essentially
    say which of his previous work is uninteresting to the current purpose of the site.
    """

    """
    :var first_name: Each author, as a person, has a first name
    """
    first_name = models.CharField(max_length=100)

    """
    :ivar last_name: Each author, as a person, also has a last name
    """
    last_name = models.CharField(max_length=100)

    # You can edit this, but if you leave it empty it will be generated automatically
    """
    :ivar slug: This is a slug field, which acts as the primary key for the model. This obviously means that it has to 
               be unique. So each author is uniquely identified by it's slug, the slug is usually meant to be composed 
               of the lower case versions of first and last name. If two authors share the exact same name then, it 
               would be required to add some additional feature such as a number. 
    """
    slug = models.SlugField(max_length=255,
                            unique=True,
                            primary_key=True)

    """
    :ivar blacklisted_institutions: This defines a many to many relation for institutions. All institutions inside this 
                                   list will be considered unimportant for the application.
    """
    blacklisted_institutions = models.ManyToManyField('Institution',
                                                      through='Blacklisting',
                                                      blank=True,
                                                      null=True,
                                                      related_name='blacklisting_meta_authors')

    """
    :ivar default_pof_structure: This field can be used to define the default pof structure for this author. The POF 
                                structure is an important property of a *publication* within the KITOpen database.
                                for a better explanation see the Author model. This optional field enables to enter a 
                                default pof structure, which is usually assumed to apply to all the publications, which 
                                were written by this author.
    """
    default_pof_structure = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self) -> str:
        """
        Returns the string representation of an author.

        **Example**

        The string representation of an author looks like the following format:
        "MetaAuthor(slug={slug}, full_name={first_name last_name})"

        :return:
        """
        return "MetaAuthor(slug='{}', full_name='{}')".format(
            self.slug,
            self.full_name
        )

    # UTILITY METHODS
    # ---------------

    @property
    def separated_name(self) -> str:
        """
        Returns the last name of an author komma whitespace and then the first name.

        :return: string
        """
        return "{last}, {first}".format(
            first=self.first_name,
            last=self.last_name
        )

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the author as the first and last name separated by a whitespace.

        :return:
        """
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name
        )


# MANY-TO-MANY "THROUGH" MODELS


class Authoring(models.Model):
    """
    Represents a many to many link between an author and a publication.

    **Details**

    The name "authoring" is a creation supposed to indicate the relationship between an author and his work. This type
    of relation is obviously of the type "many to many" since one author can have multiple publications but one
    publication can have many authors. And the way to realize such a many to many relation in django/sql is to create
    a new table which links them together. So the existence of an authoring model with author A and publication P
    indicates, that A has authored P.
    """
    # Since this model only describes the relationship between two other models, as fields we only need to set the
    # foreign key relations two both of these models. These two will then be connected through this one.
    # NOTE: It might be important to use the model.SET_NULL method for "on_delete" here!

    """
    :ivar author: The foreign relation to the author model
    """
    author = models.ForeignKey('Author',
                               related_name='authorings',
                               on_delete=models.SET_NULL,
                               null=True)

    """
    :ivar publication: The foreign relation to the publication model.
    """
    publication = models.ForeignKey('Publication',
                                    related_name='authorings',
                                    on_delete=models.SET_NULL,
                                    null=True)

    """
    :ivar index: This is a automate time field, which means that it contains a float value for the exact seconds of time 
                for the moment this authoring has been added into the database. So a timestamp basically. This is 
                actually kind of a "hack". The authorings need to be returned in the order in which they were inserted. 
                Since I could not make it work any other way, they are simply being sorted by this insertion time stamp 
                now.
    """
    index = models.TimeField(auto_now=False, auto_now_add=True)


class Affiliation(models.Model):
    """
    Represents a many to many link between an author and an institution.

    **Details**

    If an affiliation object exists, that indicates that the given author is or has been affiliated with the given
    institution. In this case "being affiliated" with an institution means, that the author has worked in the name of
    this publication (using their funds) to produce some research.
    """
    # Since this model only describes the relationship between two other models, as fields we only need to set the
    # foreign key relations two both of these models. These two will then be connected through this one.
    # NOTE: It might be important to use the model.SET_NULL method for "on_delete" here!

    """
    :ivar author: The foreign key relation towards the author model.
    """
    author = models.ForeignKey('Author',
                               related_name='affiliations',
                               on_delete=models.SET_NULL,
                               null=True)

    """
    :ivar institution: The foreign key relation towards the institution model.
    """
    institution = models.ForeignKey('Institution',
                                    related_name='affiliations',
                                    on_delete=models.SET_NULL,
                                    null=True)


class Blacklisting(models.Model):
    """
    Represents a many to many link between a meta author and an institution.

    **Details**

    If a blacklisting object exists, that indicates that the given meta author blacklists the given institution.
    Specifically this means that all work that has been done by this author while working for this institution is
    supposed to be disregarded by the functionality of the pubs app, because it is not relevant to the current work
    of the author.
    """
    # Since this model only describes the relationship between two other models, as fields we only need to set the
    # foreign key relations two both of these models. These two will then be connected through this one.
    # NOTE: It might be important to use the model.SET_NULL method for "on_delete" here!

    """
    :ivar meta_author: This is the foreign key relation towards the meta author model
    """
    meta_author = models.ForeignKey('MetaAuthor',
                                    related_name='blacklistings',
                                    on_delete=models.SET_NULL,
                                    null=True)

    """
    :ivar institution: This is the foreign key relation towards the institution model
    """
    institution = models.ForeignKey('Institution',
                                    related_name='blacklistings',
                                    on_delete=models.SET_NULL,
                                    null=True)
