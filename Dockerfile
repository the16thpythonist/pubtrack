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
WORKDIR code

EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - pubtrack.wsgi:application
