# Dockerfile based on: https://github.com/oweidner/docker.openmpi/blob/master/Dockerfile
# Build this image: docker build -t mpc .

FROM ubuntu:20.04

MAINTAINER Pierre-Francois Wolfe <pwolfe@bu.edu>

ENV USER mpc

ENV HOME=/home/${USER}

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt-get install -y --no-install-recommends sudo apt-utils && \
    apt-get install -y --no-install-recommends openssh-server \
    make gcc libopenmpi-dev openmpi-bin libsodium23 libsodium-dev && \
    apt clean && \
    apt purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -ms /bin/bash mpc

COPY src/* /home/${USER}/src/
COPY experiments/* /home/${USER}/experiments/
COPY tests/* /home/${USER}/tests/

WORKDIR /home/${USER}/experiments
RUN make exp-exchange

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

CMD mpirun -np 3 exp-exchange 1000
