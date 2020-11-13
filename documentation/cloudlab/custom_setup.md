# Custom CloudLab Configuration

1. Using a geni-lib script it is possible to create an RSpec file that defines the hardware in an experiment on CloudLab.
1. We created such a file as a profile on CloudLab, a copy of the script can be found under /scripts/ring_cl_test.py
1. Using this we can pick out specific hardware (mostly tested on the Utah cluster with m400 nodes so far). Additionally, we use a LAN rather than links between each node (links appear to consume physical connections). We can specify IP addresses for each node on the LAN making it easier to run mpi once we are setup.
1. In the scripts folder setup.sh defines the dependency and build steps for CloudLab to run on each node. in the scripts folder package_cl_setup.sh selects just the MPC source code and the setup.sh script and places them into a tar.gz file. This file is specified in the geni-lib script at a public url on DropBox. In this fashion, CloudLab can obtain the tar.gz and unpack it to each node. It can then install the dependencies on each node and automatically build the MPC codebase. Once the experiment is provisioned, tests can immediately be run.
1. For example perform the following:
  ```
  # On local machines run:
  ./package_cl_setup.sh
  # Copy file to hosting site and place URL in package_cl_setup.sh
  # Copy the modified script into CloudLab as a new profile
  # Launch an experiment using this profile
  # Pick Utah and m400 nodes (for example)
  # Add ssh key to ssh-agent if needed
  source add_cl_key_to_agent.sh
  # Once launched, ssh to node-0
  ssh -A -p 22 <name>@<node>.<cluster>.cloudlab.us
  # ssh to other nodes to confirm adding host to known connections list
  ssh 192.168.1.2
  ssh 192.168.1.3
  # Move to directory and launch experiment
  cd /home/mpc/experiments
  mpirun --host localhost,192.168.1.2,192.168.1.3 -np 3 exp-exchange 1000
  ```
1. Note: currently the setup.sh script does not seem to run automatically so perform the following until resolved:
  ```
  # Navigate to /home/mpc/ on each node
  sudo su
  ./setup.sh
  # Proceed with running mpirun commands
  ```
1. Example of launched experiment:
  ![cloudlab_custom1](/Images/cloudlab_custom1.png)
  
