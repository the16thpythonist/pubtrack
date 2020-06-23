*******************
General Information
*******************

This chapter contains general information about the pubtrack application. This includes its purpose, how it works and
what functionality it offers. The last section will be a rough overview of the architecture of the application for
development purposes. This section meant to provide only a small overview, further details being provided in the
development chapter.

Purpose
=======

Motivation
----------

The application idea originated from the Institute for Data Processing and Electronics (IPE) at the Karlsruhe Institute
of Technology (KIT).

In germany, scientific institutes are often required to undergo a periodic evaluation of their research quality, to
ensure, that research funding is well spent and will continue to be granted to that institute.
A big factor for these evaluations is metrics about the recent publications, which have been produced using the
institutes funding. Additionally to other databases such as Elsevier's *Scopus database*, at the KIT, publications are
also registered within an internal database, called *KITOpen*.

And usually publication metrics could easily be generated using the KITOpen database, but this often produces incomplete
results with less publications, that it actually should be. This is due to 2 reasons:

1. Some publications might not be registered in KITOpen, because the authors forgot to insert them or some other reason

2. When inserting a new publication, a parameter called *POF Structure* can be associated with a publication to
identify from which plan the publication assets where funded. This is then later used to associate a publication with
a certain institute. The problem is that these POF identifiers are often missing or switched up.

Dut to these reasons, it is often required to manually check all the publications to generate the publication metrics
and to fix the identifiers within the system.

Aim
---

This is what the *pubtrack* application was designed for. It is meant to be a management application, which
*keeps track* of all the publications of an institute and their associated parameters, creating status alerts in case
it was not found on KITOpen for example and also providing the means to resolve the issue all in one platform.


Functionality
=============

Features
--------

tbd

Architecture
============

Working Principle
-----------------

So this is the basic timeline of how the application works:

1. The user of the application defines a set of *authors*, which are to be observed. These observed authors essentially
provide the means of keeping track of the happenings within an institution. One such observed author profile has to
contain information such as first and last name. It can additionally be linked to one or more scopus author profiles

2. The information within these author profiles is used to query both Scopus *and* KITOpen for all of their information
regarding the authors latest publications. This publication information is then stored within the backend database.

3. From all the data of a publication a status and thus a potential warning can be computed for each publication. An
example would be that the POF structure of a publication does not match the predefined POF structure of the institute.
In this case a warning would be created informing the user of a potentially switched entry of the POF structure

4. The user can choose how to handle the errors. In some cases they may just be a false alert and can be ignored. If
the warning does actually refer to a problem, the site offers predefined actions, which help to resolve the issue as
quickly as possible. In the case of the above example this could be a pre-generated email body, which will inform the
KITOpen support of the faulty entry.

Implementation
--------------

