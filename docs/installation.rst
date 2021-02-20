============
Installation
============

Installing on a standalone Linux Server
---------------------------------------

Requirements
~~~~~~~~~~~~

The pubtrack application is fully dockerized and thus essentially only needs docker and docker-compose to work
properly. Aside from that curl is used inside the installation script.

.. code-block:: console

    $ sudo apt-get install docker docker-compose curl

Installing Docker on Raspberry Pi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the application is supposed to be deployed on a Raspberry Pi, docker cannot be simply installed using the
system package manager. Instead execute the following commands:

.. code-block:: console

    $ sudo apt-get update
    $ curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    $ sudo bash /tmp/get-docker.sh

Installation
~~~~~~~~~~~~

To install the production version of the application on a linux server follow these steps:

**(1)** Fetch the source code from Github.

.. code-block:: console

    $ git clone https://github.com/the16thpythonist/pubtrack.git

**(2)** Set the environmental variable `PUBTRACK_DOMAIN` to the domain name, which will be used to
access the application. If the application is only supposed to be used on the local machine supply
"localhost" as the default value.

.. code-block:: console

    $ export PUBTRACK_DOMAIN="localhost"

**(3)** Navigate into the source code folder and run the `install.sh` script. The installation requires
a working network connection and may take multiple minutes. At the end of the installation the user will
be prompted to supply credentials for the admin user profile of the application.

.. code-block:: console

    $ sudo bash install.sh

**(4)** Run the application

.. code-block:: console

    $ sudo docker-compose -f production.yml up

Tested Platforms
~~~~~~~~~~~~~~~~

- Ubuntu 20.04 LTS
- Raspberry Pi 3, Debian Jessie
- Raspberry Pi 4, Debian Buster


Installing on OpenShift
-----------------------

The installation on OpenShift is slightly more complicated than the installation on a standalone server, because there
are more manual steps involved. In the future it would be nice to have a script, which wraps this.

**NOTE:** The following sections will provide a step-by-step guide for the installation. All text within the console
examples, which is enclosed by curled brackets is supposed to be replaced with values that are appropriate with your
own setup! Within these curled brackets, there will be an example for how that value might look like. But it is
important to not copy the curled brackets, when following this guide!

Installing Postgres
~~~~~~~~~~~~~~~~~~~

The first step is to deploy a new postgres database application in your OpenShift project, which the pubtrack
application will be able to use.

The following repository provides the necessary Dockerfile to create a new OpenShift postgres image:
https://github.com/sclorg/postgresql-container/tree/generated/10

Build a new postgres image.

.. code-block:: console

    $ oc new-build --name={postgres} \
                   --strategy=docker \
                   --context-dir="10" https://github.com/sclorg/postgresql-container.git#generated

**TODO:** How to add persistent volume mount.