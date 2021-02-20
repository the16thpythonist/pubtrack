FROM python:3.8
MAINTAINER Jonas Teufek <jonseb1998@gmail.com>
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# INSTALLING NPM AND NODE
# ***********************

# and install dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get -y autoclean

# Using Debian, as root
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs

# confirm installation
RUN node -v && \
    npm -v

# Install Vue CLI
# I think this is not even necessary?
# RUN npm install -g @vue/cli

# Adds our application code to the image
ENV APP_ROOT=/code

COPY . ${APP_ROOT}
COPY ./README.md ${APP_ROOT}/pubtrack/README.md

# This is necessary in OpenShift to support arbitrary user ID's
RUN chgrp -R 0 ${APP_ROOT} && \
    chmod -R g=u ${APP_ROOT} /etc/passwd

WORKDIR ${APP_ROOT}
RUN mkdir ${APP_ROOT}/static && \
    chmod -R 0777 ${APP_ROOT}/static && \
    chmod -R 0777 ${APP_ROOT}/pubtrack/frontend && \
    ls -la ${APP_ROOT}/pubtrack/frontend

EXPOSE 8000
USER 10001

# Note: A Dockerfile absolutely needs the "\" character when doing a multiline expression. Otherwise it will interpret
# the newline as a seperate command!
CMD bash run.sh