#!/bin/bash

set -x

docker stop my-running-script
docker rm my-running-script

pwd

docker run -t --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.6 ./AirVisualWebAPI.py
