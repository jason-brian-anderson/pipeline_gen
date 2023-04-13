#!/bin/bash

docker system prune -f
docker rmi $(docker images -a -q)
