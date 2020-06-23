General Information
*******************

This chapter contains general information about the pubtrack application. This includes its purpose, how it works and
what functionality it offers. The last section will be a rough overview of the architecture of the application for
development purposes. This section meant to provide only a small overview, further details being provided in the
development chapter.

Purpose
-------

Motivation
^^^^^^^^^^

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
^^^

This is what the *pubtrack* application was designed for.



Functionality
-------------

lol

Architecture
------------

lol