************
Installation
************

Installing on a Linux Server
============================

To install the production version of the application on a linux server follow these steps:

0) Install docker compose on the system, if it is not already installed

.. code-block:: bash
    sudo apt-get install docker-compose

1) Fetch the source code from Github.

.. code-block:: bash

    $ git clone https://github.com/the16thpythonist/pubtrack.git

2) Navigate into the source code folder and run the `build.sh` script

.. code-block:: bash

    $ bash build.sh

Tested Platforms
----------------

- Raspberry Pi 4, Debian Buster