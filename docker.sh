#!/usr/bin/env bash

source ./docker/.env

sha=$(git rev-parse --short HEAD)
tag="dev"
mode=$1
[[ -z $mode ]] && mode=runtime
echo $mode

DOCKER_BUILDKIT=1 docker build \
    --build-arg "MAINTAINER=$APP_MAINTAINER" \
    --build-arg "APP_VERSION=$APP_VERSION" \
    --build-arg "BASE_IMAGE_VERSION=$PYTHON_VERSION" \
    --build-arg "COMMIT_SHA=$sha" \
    -t rubix-service:"$tag"\
    --progress=plain \
    -f "$(pwd)/docker/$mode.Dockerfile" \
    ./ || { echo "Build $tag failure"; exit 2; }

docker rmi $(docker images | grep "none" | awk '/ / { print $3 }') || exit 0
