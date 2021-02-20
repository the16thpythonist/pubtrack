#!/bin/bash
# The following env variables have to exist for this script to work:
# - PUBTRACK_DOMAIN: The public domain name under which pubtrack will be accessible
# - PUBTRACK_PORT: The port under which the pubtrack application will be listening. Important: In the background, the
#   the port 8000 will always be used. This variable refers only to the case in which there is a redirection as with
#   openshift for example. On default this should always be 8000.
# - POSTGRES_USER: The username for the postgres database
# - POSTGRES_PASSWORD: The password for the postgres database
# - POSTGRES_DB: The database name
# - POSTGRES_HOST: The hostname under which the postgres database is accessible

# TODO: Explain this code
echo "==| (OPTIONAL) OPENSHIFT PERMISSIONS |=="
if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi

echo "==| WAITING FOR POSTGRES |=="
python wait_for_postgres.py

echo "==| COMPILING FRONTEND CODE |=="
cd /code/pubtrack/frontend
npm install
export VUE_APP_API_URL="http://$PUBTRACK_DOMAIN:$PUBTRACK_PORT/api/v1/"
npm run build

echo "==| STATIC FILES AND MIGRATIONS |=="
cd /code
python manage.py collectstatic --noinput --configuration Production
python manage.py makemigrations
python manage.py migrate

echo "==| STARTING SERVER |=="
python manage.py runserver --configuration=Production 0.0.0.0:8000