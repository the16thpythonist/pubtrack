# pubtrack

[![Build Status](https://travis-ci.org/the16thpythonist/pubtrack.svg?branch=master)](https://travis-ci.org/the16thpythonist/pubtrack)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Tracking author publications for KIT-IPE. Check out the project's [documentation](http://the16thpythonist.github.io/pubtrack/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Create a new admin user for the django website

```bash
docker-compose run --rm web python manage.py createsuperuser
```

Create the new migrations.
No worries though you dont have to apply them. This is automatically being done each time the server is started

```bash
docker-compose run --rm web python manage.py makemigrations
```

Delete all database records

```bash
docker-compose run --rm web python manage.py flush
```
