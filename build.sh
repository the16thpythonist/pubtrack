#!/usr/bin/env bash

sudo docker-compose -f production.yaml build

cd pubtrack/frontend
sudo npm install
sudo npm run build
