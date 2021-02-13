# INSTALLING THE N NODE VERSION MANAGER
# =====================================
# In case the temporary version of the node package manager already exists.
# We want to delete it first before making a fresh download.
# This is really only important when executing the script consecutively.
if [ -f /tmp/n ]
  then
    rm /tmp/n
fi
curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o /tmp/n
bash /tmp/n lts
sudo chmod +x /tmp/n

# INSTALLING THE CORRECT NODE VERSION
# ===================================

if [ "$(npm --version)" ]
  then
    sudo /tmp/n install 10.22.1
    echo "NODE VERSION: $(node --version)"
    echo "NPM VERSION: $(npm --version)"
  else
    echo "NODE and NPM are already installed"
fi

# INSTALLING THE FRONTEND CODE
# ============================
echo "Starting to build the frontend code"
echo "PUBTRACK_DOMAIN=$PUBTRACK_DOMAIN"
cd ./pubtrack/frontend
sudo npm install
sudo VUE_APP_API_URL="http://$PUBTRACK_DOMAIN:8000/api/v1/" npm run build

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
# This line right here is the only line which will trigger user input. The user
# will be prompted to create an initial user for the database by putting in
# a username and a password.
sudo docker-compose -f production.yml run web python manage.py createsuperuser


