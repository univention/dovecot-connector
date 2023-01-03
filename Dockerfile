# syntax=docker/dockerfile:1

ARG DOCKERHUB_CACHE=""

###############################################################################
FROM ${DOCKERHUB_CACHE}library/debian:bullseye-slim AS debian-python3-builder
SHELL ["/bin/sh", "-eux", "-c"]

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -V install --assume-yes --verbose-versions --no-install-recommends \
      # dependency of stdeb \
      python3-all \
      # for python3 executable \
      python3-minimal \
      # for setuptools module \
      python3-setuptools \
      # for py2dsc executable \
      python3-stdeb


###############################################################################
FROM ${DOCKERHUB_CACHE}library/alpine:3.12 AS dovecot-connector-alpine-build
SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

ARG version

# Build a Wheel-Package for univention-dovecot-connector
WORKDIR /build/univention-dovecot-connector

RUN \
  apk add --no-cache python3 py3-pip && \
  python3 -m venv --system-site-packages /build/venv && \
  /build/venv/bin/python3 -m pip install --upgrade pip && \
  /build/venv/bin/pip3 install build

COPY univention-dovecot-connector /build/univention-dovecot-connector
RUN \
  export DOVECOT_PROVISIONING_VERSION="$version" && \
  /build/venv/bin/python3 -m build && \
  mkdir /pippkg && \
  cp -a /build/univention-dovecot-connector/dist/*.whl /pippkg/ && \
  rm -rf /build/


###############################################################################
FROM ${DOCKERHUB_CACHE}library/debian:bullseye-slim AS final
SHELL ["/bin/sh", "-eux", "-c"]

ARG version

LABEL \
  "description"="UCS dovecot provisioning app" \
  "version"="$version"

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -V install --assume-yes --verbose-versions --no-install-recommends \
      # for dbm.gnu useed by listener_trigger
      python3-gdbm \
      # for the python3 executable \
      python3-minimal \
      # for the pip3 executable \
      python3-pip \
      # for python-doveadm
      python3-requests \
      unzip

# install python-doveadm
WORKDIR /pkg-temp/python-doveadm
COPY python-doveadm.zip .
RUN \
  ls -la && \
  unzip -d . python-doveadm.zip && \
  ls -la && \
  dpkg -i *.deb && \
  rm -rf /pkg-temp/

# install dovecot-connector
WORKDIR /pkg-temp
COPY --from=dovecot-connector-alpine-build /pippkg/*.whl /pkg-temp/
RUN \
  pip install /pkg-temp/*.whl && \
  rm -r /pkg-temp

COPY init.py /sbin/init.py
COPY LICENSE /usr/local/share/dovecot-connector/LICENSE
RUN chmod 0555 /sbin/init

WORKDIR /dovecotp

CMD ["/usr/bin/python3", "-u", "/sbin/init.py"]

# [EOF]
