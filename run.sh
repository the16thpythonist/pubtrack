#!/usr/bin/env bash

sudo docker kill $(sudo docker ps -a -q)
sudo docker-compose -f production.yaml up
