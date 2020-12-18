#!/usr/bin/env bash

source ./docker/.env

sha=$(git rev-parse --short HEAD)
tag="dev"

DOCKER_BUILDKIT=1 docker build \
    --build-arg "MAINTAINER=$APP_MAINTAINER" \
    --build-arg "APP_VERSION=$APP_VERSION" \
    --build-arg "PYTHON_VERSION=$PYTHON_VERSION" \
    --build-arg "COMMIT_SHA=$sha" \
    -t rubix-service:"$tag"\
    --progress=plain \
    -f "$(pwd)/docker/Dockerfile" \
    ./ || { echo "Build $tag failure"; exit 2; }

docker rmi $(docker images | grep "none" | awk '/ / { print $3 }') || exit 0
