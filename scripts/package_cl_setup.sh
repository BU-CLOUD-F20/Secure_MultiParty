#!/bin/bash

# Bundle MPC Source code and Installer script for CloudLab
# MPC tests and experiements on Ubuntu 20.04 setup

# -c : creates a new archive
# -z : uses gzip compression
# -f : specifies files to be added
# In this case I only want *.c, *.h, and Makefile
# I use some regex in the paths specified to achieve this
tar -czf cloudlab_setup.tar.gz ../src/*[.][ch] ../tests/{*[.][ch],Makefile} ../experiments/{*[.][ch],Makefile} setup.sh
