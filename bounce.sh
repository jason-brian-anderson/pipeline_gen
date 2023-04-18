#!/bin/bash
#BE CAREFUL - as you can see below, this nukes your docker env from high orbit.

docker-compose down
./clean_docker.sh
./build_pipeline_image.sh
docker-compose up
