ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-alpine as build

RUN apk add git curl \
        gcc g++ make file musl-dev linux-headers \
        libc-dev zlib zlib-dev libffi libffi-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /usr/src/app/
ADD poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ADD src src
ADD systemd systemd
ADD run.py ./
RUN $HOME/.poetry/bin/poetry run pyinstaller run.py -n rubix-service --clean --onefile \
    --add-data pyproject.toml:. \
    --add-data systemd:systemd

FROM python:$BASE_IMAGE_VERSION-alpine

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV GLOBAL_DATA=/data RUBIX_SERVICE_DATA=/data/rubix-service ARTIFACT_DIR=/data/apps RUBIX_SERVICE_TOKEN=''

RUN addgroup --system --gid $NUBEIO_GID nubeio \
    && adduser --system -G nubeio --uid $RUBIX_UID rubix \
    && mkdir -p $RUBIX_SERVICE_DATA \
    && chown -R rubix:nubeio $RUBIX_SERVICE_DATA

WORKDIR /usr/src/app/
COPY --chown=rubix:nubeio --from=build /usr/src/app/dist/rubix-service ./

USER rubix:nubeio

VOLUME $GLOBAL_DATA

EXPOSE 1616

ENTRYPOINT [ "./rubix-service" ]
