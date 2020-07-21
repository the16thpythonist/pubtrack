#!/usr/bin/env bash

cd pubtrack/frontend
sudo npm run build

cd ../..
sudo docker-compose -f production.yml up
