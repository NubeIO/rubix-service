ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim-buster as build

RUN apt update -qq
RUN apt install git -y
RUN apt install curl -y
RUN apt install gcc -y
RUN apt install g++ -y
RUN apt install make -y
RUN apt install file -y
RUN apt install musl-dev -y
RUN apt install libffi-dev -y
RUN apt install zlib1g -y
RUN apt install zlib1g-dev -y
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=1.1.13 python3

WORKDIR /usr/src/app/
ADD poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ADD src src
ADD config config
ADD systemd systemd
ADD run.py VERSION ./
RUN $HOME/.poetry/bin/poetry run pyinstaller run.py -n rubix-service --clean --onefile \
    --add-data VERSION:. \
    --add-data config:config \
    --add-data systemd:systemd

FROM python:$BASE_IMAGE_VERSION-slim

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV GLOBAL_DATA=/data RUBIX_SERVICE_DATA=/data/rubix-service ARTIFACT_DIR=/data/apps

RUN groupadd -g $NUBEIO_GID nubeio \
    && useradd -u $RUBIX_UID -G nubeio rubix \
    && mkdir -p $RUBIX_SERVICE_DATA \
    && chown -R rubix:nubeio $GLOBAL_DATA

RUN apt update -qq \
    && apt install curl sudo -y --no-install-recommends \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install nodejs -y --no-install-recommends\
    && usermod -a -G sudo rubix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY --chown=rubix:nubeio --from=build /usr/src/app/dist/rubix-service ./

USER rubix:nubeio

VOLUME $GLOBAL_DATA

EXPOSE 1313 1414 1515 1616 1717 1919 1880 8081

ENTRYPOINT [ "./rubix-service" ]
