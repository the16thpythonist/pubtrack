FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt


# INSTALLING NPM AND NODE
# ***********************

# and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# Using Debian, as root
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y nodejs

# confirm installation
RUN node -v
RUN npm -v

# Install Vue CLI
RUN npm install -g @vue/cli

# Adds our application code to the image
COPY . code
COPY ./README.md code/pubtrack/README.md

# This is necessary in OpenShift to support arbitrary user ID's
RUN chgrp -R 0 /code \
    chmod -R g=u /code

WORKDIR /code
RUN mkdir /code/static && chmod -R 0777 /code/static

EXPOSE 8000
USER 1001

# Note: A Dockerfile absolutely needs the "\" character when doing a multiline expression. Otherwise it will interpret
# the newline as a seperate command!
CMD bash run.sh