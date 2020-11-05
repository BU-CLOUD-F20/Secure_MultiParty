#!/bin/bash

# Based on example here: https://pythonspeed.com/articles/system-packages-docker/
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

# Check for and then install updates
apt-get update
apt-get -y upgrade

# Install additional packages
apt-get -y install build-essential openmpi-bin libsodium23 libsodium-dev
apt autoclean
apt autoremove
rm -rf /var/lib/apt/lists/*
