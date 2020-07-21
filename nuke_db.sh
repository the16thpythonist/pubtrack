sudo docker-compose run --rm web python manage.py reset_db --noinput
sudo rm -r pubtrack/pubs/migrations/
sudo docker-compose run --rm web python manage.py makemigrations pubs
sudo docker-compose run --rm web python manage.py migrate
sudo docker-compose run --rm web python manage.py createsuperuser