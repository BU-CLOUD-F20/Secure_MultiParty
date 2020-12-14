#!/bin/bash

# Installer script for CloudLab

# Check Linux Version
OS=`lsb_release -i | cut -f2`
RELEASE=`lsb_release -r | cut -f2`

# Alternate approach...use this to support CentOS eventually...
#grep ^NAME /etc/os-release

# Ubuntu
if [[ $OS == "Ubuntu" ]]; then
  # Perform update
  apt update -y && apt upgrade -y
  # Install dependencies
  if [[ $RELEASE == "16.04" ]]; then
    apt install -y make gcc libopenmpi-dev openmpi-bin libsodium18 libsodium-dev
  elif [[ $RELEASE == "18.04" ]]; then
    apt install -y make gcc libopenmpi-dev openmpi-bin libsodium23 libsodium-dev
  elif [[ $RELEASE == "20.04" ]]; then
    apt install -y make gcc libopenmpi-dev openmpi-bin libsodium23 libsodium-dev
  else
    echo "Some other Ubuntu version"
  fi

# Other
else
  echo "Not Ubuntu"
fi

# Build MPC codebase (This will only work if the dependencies were successfully installed)
cd experiments
make all

# Now we're done with setup and can run something like this:
# mpirun --host localhost,192.168.1.2,192.168.1.3 -np 3 hostname
# mpirun --host localhost,192.168.1.2,192.168.1.3 -np 3 exp-exchange 1000
