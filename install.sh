# INSTALLING THE N NODE VERSION MANAGER
# =====================================
curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o /tmp/n
bash /tmp/n lts
sudo chmod +x n

# INSTALLING THE CORRECT NODE VERSION
# ===================================
sudo /tmp/n install 10.22.1
echo "NODE VERSION: $(node --version)"
echo "NPM VERSION: $(npm --version)"

# INSTALLING THE FRONTEND CODE
# ============================
cd ./pubtrack/frontend
sudo npm install
sudo VUE_APP_API_URL="http://$PUBTRACK_DOMAIN/api/v1/" npm build
#sudo VUE_APP_API_URL="https://localhost/api/v1" npm build


# BUILDING THE DOCKER CONTAINERS
# ==============================
cd ../..
sudo docker-compose -f production.yml build

# APPLYING DATABASE MIGRATIONS
# ============================
sudo docker-compose -f production.yml run web python manage.py makemigrations pubs
sudo docker-compose -f production.yml run web python manage.py migrate

# CREATING A NEW SUPER USER
# =========================
sudo docker-compose -f production.yml run web python manage.py createsuperuser


