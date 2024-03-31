#!/bin/bash

docker rmi -f geminal

docker build --build-arg GOOGLE_API_KEY=$(echo "$GOOGLE_API_KEY") -t geminal .