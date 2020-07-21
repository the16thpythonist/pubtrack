#!/usr/bin/env bash

sudo docker-compose -f production.yaml build

cd pubtrack/frontend
sudo npm run build
