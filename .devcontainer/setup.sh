#!/bin/bash 

# Milvus database setup
## Get docker-compose.yml
wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose.yml -O docker-compose.yml
## Run docker-compose
docker-compose up -d
## Check connection
docker port milvus-standalone 19530/tcp
## To remove:
# docker compose down
# rm -rf  volumes


