***********
Development
***********

This is the section for setting up the development environment for the pubtrack web application.

The basic scaffold of the backend application using Django REST was created using *python cookicutter* especially
the template *cookiecutter-django-rest*. If there are any issues with the development environment, it might be
worth to also check out their documentation.

The development environment for this application is heavily based on the usage of *Docker containers*. Even though
it should also work without the docker environment, it has not been tested without and thus it is strongly encouraged
to used the container setup.

A note on the operating systems
"""""""""""""""""""""""""""""""

Since the application is running within docker containers, the development setup should theoretically be operating
system agnostic. It has only been tested on a linux machine (Ubuntu LTS 18) however.

Requirements
------------

As mentioned before, the development makes heavy usage of Docker containers. So if not already installed, make sure to
install both *docker* and *docker-compose*

.. code-block:: bash

    $ sudo apt-get install docker
    $ sudo apt-get install docker-compose

Setting Up
----------

To set up the local environment, the docker containers fist have to be built:

.. code-block:: bash

    $ sudo docker-compose -f development.yml build

After the containers have been build, a new admin account has to be created for the django backend of the
application. Running this command will most likely first build the "postgres" container of the application first, as
that is not included in the build process above. The command will prompt for input of a admin username and password.

.. code-block:: bash

    $ sudo docker-compose -f development.yml run web python3 manage.py createsuperuser

Then the necessary django migrations have to be applied to the new database with the following commands.

.. code-block:: bash

    $ sudo docker-compose -f development.yml run web python3 manage.py makemigrations pubs
    $ sudo docker-compose -f development.yml run web python3 manage.py migrate

At last the necessary node modules have to be installed for the front end code. Simply navigate to the frontend folder
and install the packages.

.. code-block:: bash

    $ cd pubtrack/frontend
    $ sudo npm install

Running the App
---------------

To run the whole system simply use the following command.

.. code-block:: bash

    $ sudo docker-compose -f development.yml up

This command will simultaneously run the Django backend and the frontend application as local servers. The result can
be viewed by visiting `http://0.0.0.0:8000`. This development setup features dynamic changes in both backend and
frontend code. Every modification made to a code file will be automatically detected and loaded by the local servers
once the modified file has been saved. Thus changes can be made in real time.

