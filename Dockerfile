# syntax=docker/dockerfile:1

ARG UCS_BASE_IMAGE_TAG=v0.7.5
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-520

###############################################################################
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS debian-python3-builder
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

RUN \
  apt-get update -qq && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get install --assume-yes --verbose-versions --no-install-recommends \
      # dependency of stdeb \
      python3-all \
      # for python3 executable \
      python3-minimal \
      # for setuptools module \
      python3-setuptools \
      # for py2dsc executable \
      python3-stdeb


###############################################################################
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS dovecot-connector-build
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

ARG version

# Build a Wheel-Package for univention-dovecot-connector
WORKDIR /build/univention-dovecot-connector

RUN \
    apt-get update -qq && \
    apt-get install --assume-yes --verbose-versions --no-install-recommends \
      python3-minimal \
      python3-pip \
      python3-venv && \
  python3 -m venv /build/venv && \
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
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS final
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

ARG version

LABEL \
  "description"="UCS dovecot provisioning app" \
  "version"="$version"

RUN \
  apt-get update -qq && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get install --assume-yes --verbose-versions --no-install-recommends \
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
  unzip -d . python-doveadm.zip && \
  dpkg -i *.deb && \
  rm -rf /pkg-temp/

# install dovecot-connector
WORKDIR /pkg-temp
COPY --from=dovecot-connector-build /pippkg/*.whl /pkg-temp/
RUN \
  pip3 install --break-system-packages /pkg-temp/*.whl && \
  rm -r /pkg-temp

COPY init.py /sbin/init.py
COPY LICENSE /usr/local/share/dovecot-connector/LICENSE
RUN chmod 0555 /sbin/init.py

WORKDIR /dovecotp

CMD ["/usr/bin/python3", "-u", "/sbin/init.py"]

# [EOF]
