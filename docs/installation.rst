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

    $ oc new-build https://github.com/sclorg/postgresql-container.git#generated \
                   --name={postgres} \
                   --strategy=docker \
                   --context-dir="10"

Then you'll have to wait until the image is built. After the image is built you can create a new deployment config with
from this image.

**NOTE:** It is possible to create a new deployment config from the command line, but I would recommend to use the
web console. The reason is this: There could be a chance that your "oc" version is not entirely compatible with the
version of your openshift cluster. This could lead to the problem that oc tries to create a deployment config with an
unsupported tag, which leads to an error. So just do it in the console.

In the OpenShift web console then navigate to *"Add to project"* in the upper right corner of the UI. Select the
option *"From imagestream"*. Within this window select the namespace to be your project, the image name *"{postgres}"*
is the name which you have previously given to the build. The tag will be *"latest"*.

Then it is also important to define the following environmental variables for the postgres deployment, which will
manage the access to the database:

- `POSTGRESQL_USER`: {dbuser}
- `POSTGRESQL_PASSWORD`: {dbpassword}
- `POSTGRESQL_DATABASE`: {dbname}

After confirming the action, a new deployment will be started.

**TODO:** How to add persistent volume mount.

Installing Pubtrack
~~~~~~~~~~~~~~~~~~~

First build the pubtrack image from it's repository:

.. code-block:: console

    $ oc new-build https://github.com/the16thpythonist/pubtrack.git \
                   --name={pubtrack} \
                   --strategy=docker \
                   --env="PUBTRACK_DOMAIN={pubtrack.mydomain.com}"

During this step it is important, that you pass the env variable `PUBTRACK_DOMAIN`, which contains the public url name
which pubtrack will be using later on. You will have to create this name later on as a *OpenShift Route*. It will be a
sub domain of the general domain which your cluster has.

This build process might take several minutes. After it is done create a deployment using the Web console.

In *"Add to project"* select *"from imagestream"*. Select your project name as the namespace, *"{pubtrack}"* image and
the *"latest"* tag.

Supply the following environmental variables:

- `DJANGO_SECRET_KEY`: {random string}
- `POSTGRES_USER`: {dbuser}
- `POSTGRES_PASSWORD`: {dbpassword}
- `POSTGRES_DB`: {dbname}
- `POSTGRES_HOST`: {postgres}

After confirming the action, the new deployment will start.

At last, you will have to create a new route for the pubtrack service. For this, navigate to the *Routes* page within
the OpenShift web console. Add a new route with the name "{pubtrack}" and enter the value "{pubtrack.mydomain.com}".
For the service, select the "{pubtrack}" service and make sure, that it actually uses the pubtrack default port 8000.

Visit http://{pubtrack.mydomain.com}:8000 to see if it working.