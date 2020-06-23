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

.. code-block:: console

    sudo apt-get install docker
    sudo apt-get install docker-compose




