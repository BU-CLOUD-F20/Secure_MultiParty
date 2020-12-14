#!/bin/bash

# Note: For this to apply in the current shell make sure to "source" the script
# i.e. "source add_key_to_agent.sh"

# Setup ssh-agent
ssh-agent > agent_variable.tmp
source agent_variable.tmp
rm agent_variable.tmp

# Add key of interest to agent
# Modify this line to the location of the key you want to be able to load
ssh-add ~/.ssh/clab

# Enter the passphrase when prompted

# Check that the key was added
ssh-add -l

# Now ssh to the target device
# In order to forward the loaded key, use the -A flag
# e.g. "ssh -A pwolfe@128.31.25.149"
