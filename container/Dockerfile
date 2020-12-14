# Dockerfile based on: https://github.com/oweidner/docker.openmpi/blob/master/Dockerfile
# https://codeburst.io/direct-connection-to-a-docker-container-with-ssh-56e1d2744ee5
# Build this image: docker build -t mpc .

FROM ubuntu:20.04
MAINTAINER Pierre-Francois Wolfe <pwolfe@bu.edu>

ENV USER mpc
ENV HOME=/home/${USER}
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt-get install -y --no-install-recommends sudo apt-utils && \
    apt-get install -y --no-install-recommends openssh-server \
    make ssh gcc libopenmpi-dev openmpi-bin libsodium23 libsodium-dev && \
    apt clean && \
    apt purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /var/run/sshd
RUN echo 'root:${USER}' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# ------------------------------------------------------------
# Add an 'mpc' user
# ------------------------------------------------------------

RUN adduser --disabled-password --gecos "" ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ------------------------------------------------------------
# Set-Up SSH with our Github deploy key
# ------------------------------------------------------------

ENV SSHDIR ${HOME}/.ssh/

RUN mkdir -p ${SSHDIR}

ADD ssh/config ${SSHDIR}/config
ADD ssh/id_rsa.mpi ${SSHDIR}/id_rsa
ADD ssh/id_rsa.mpi.pub ${SSHDIR}/id_rsa.pub
ADD ssh/id_rsa.mpi.pub ${SSHDIR}/authorized_keys

RUN chmod -R 600 ${SSHDIR}* && \
    chown -R ${USER}:${USER} ${SSHDIR}

# ------------------------------------------------------------
# Copy MPC code
# ------------------------------------------------------------

COPY src/* /home/${USER}/code/src/
COPY experiments/* /home/${USER}/code/experiments/
COPY tests/* /home/${USER}/code/tests/
COPY launch.sh /home/${USER}/code/experiments/

WORKDIR /home/${USER}/code/experiments
RUN make exp-exchange

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

RUN chown -R ${USER}:${USER} ${HOME}/code

RUN /usr/bin/ssh-keygen -A

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
