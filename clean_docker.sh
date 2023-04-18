#!/bin/bash
#Don't run this unless you want to flush your entire docker environment
#though this will not touch previously created volumes like the postgresdb vol
docker rmi $(docker images -a -q)
docker system prune -f
docker volume prune -f

