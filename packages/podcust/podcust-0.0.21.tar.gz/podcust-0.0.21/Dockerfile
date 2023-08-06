FROM fedora:latest

RUN dnf -y update
RUN dnf -y install python3-pip python3-tox make podman-compose
RUN dnf clean all

ADD . /src

RUN cd /src; pip install --upgrade pip; pip install .[dev]
