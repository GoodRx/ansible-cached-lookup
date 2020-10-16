FROM python:3.6

WORKDIR /src

RUN apt-get update
RUN pip install -U pip tox wheel setuptools virtualenv --cache-dir=/codefresh/volume/pip-cache

COPY ansible-cached-lookup /src
