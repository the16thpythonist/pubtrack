FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Ok this needs some explaining. ARG specifies, that an argument of this name is being passed from the host system
# to the build environment. And then in the next line ENV declares a new environmental variable for the rest of this
# Dockerfile. In fact the env variable has the same name as the argument and also has its value (The value is invoked
# by the $ symbol in front of an ARG).
# Now if you look into the production.yml file, you will see, that the argument value there is in fact defined as the
# value of the env variable of the same name *on the host system* So all of this is a method of transferring the value
# of the env variable within the host system to the same env variable within the container.

# This value will actually be needed for the compilation of the frontend code, which needs a hard coded url of the
# REST API's url during compile time. So this is the way that it is passed in
ARG PUBTRACK_DOMAIN
ENV PUBTRACK_DOMAIN $PUBTRACK_DOMAIN
ENV VUE_APP_API_URL "http://$PUBTRACK_DOMAIN:8000/api/v1/"

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

# COMPILING FRONTEND APPLICATION
# ******************************

RUN echo $VUE_APP_API_URL
RUN cd /code/pubtrack/frontend \
    && npm install \
    && npm run build

WORKDIR /code

EXPOSE 8000

# Run the production server
# CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:8000 --access-logfile - pubtrack.wsgi:application

# Note: A Dockerfile absolutely needs the "\" character when doing a multiline expression. Otherwise it will interpret
# the newline as a seperate command!
CMD bash -c "echo '==| WAITING FOR POSTGRES DB |==' \
             && python wait_for_postgres.py \
             && echo '==| STATIC FILES AND DB MIGRATIONS |==' \
             && ./manage.py collectstatic --noinput --configuration Production \
             && ./manage.py migrate \
             && echo '==| STARTING WEB SERVER |==' \
             && ./manage.py runserver --configuration=Production 0.0.0.0:8000"