============
Installation
============

Installing on a Linux Server
----------------------------

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

    $ bash install.sh

**(4)** Run the application

.. code-block:: console

    $ sudo docker-compose -f production.yaml up

Tested Platforms
~~~~~~~~~~~~~~~~

- Ubuntu 20.04 LTS
- Raspberry Pi 3, Debian Jessie
- Raspberry Pi 4, Debian Buster