# Installing and testing MPI

## Initial Setup

1. Following the suggestion from INSTRUCTIONS.md we will install OpenMPI (though there are other implementations that we may want to explore in the future)
1. Rather than installing from source, as `apt search openmpi-bin` shows a build of openmpi 4.0.3 I will install through the package manager instead using `sudo apt install openmpi-bin`.
1. `ompi_info` displays information that can help to verify the installation of openmpi

    ![openmpi1](/Images/openmpi1.png)

1. Now I need to write/find a simple openmpi test to run... I found one at the following [link](https://mpitutorial.com/tutorials/mpi-hello-world/) online.
1. In order to follow the example, I copied the [example source code](https://github.com/mpitutorial/mpitutorial/blob/gh-pages/tutorials/mpi-hello-world/code/mpi_hello_world.c) to the VM and built the program using mpicc as follows: ` mpicc -o mpi_hello_world mpi_hello_world.c`
1. Subsequently I was able to run one instance of the job locally on the VM but trying to launch more than one instance resulted in a warning that the VM does not contain sufficient slots.

    ![openmpi2](/Images/openmpi2.png)

1. As noted in the warning message, I can bypass this through a number of methods including by using --oversubscribe. This functions but in the future I will want to make sure to take into consideration the number of cores that are available to a particular VM vs. how many jobs are being run. Furthermore, configuring the hostfile appears to be the correct step for specifying a long-term setting.

    ![openmpi3](/Images/openmpi3.png)

...now the next step may be to test the MPC codebase on a single node or to generate additional VMs and test the mpi hello world across them (before subsequently testing the MPC codebase) *TBD*

## Multiple Hosts

1. The following is a simple way to test that mpi is functioning correctly across multiple hosts (in this case after cloning a VM see cc-mpc-secondary_setup.md that can locally run and MPI program including the MPC code, see cc-mpc-main_setup.md)
1. Having used SSH to log into the main VM (see ssh_notes.md) run the following command using the appropriate IP addresses for the secondary VMs, the hostnames for all three should be displayed if correct communication is occurring.
```
# In our test the following command:
mpirun --host localhost,192.168.100.7,192.168.100.18 -np 3 hostname
# Returns the following:
cc-mpc-main
cc-mpc-secondary-1
cc-mpc-secondary-2
```
1. After having verified proper functioning, the tests.sh script in the test directory can be updated from `MPIRUN="mpirun -np"` to `MPIRUN="mpirun --host localhost,192.168.100.7,192.168.100.18 -np"` With this change, running the script will now launch all of the tests in order across all three VMs (assuming that the directory structure is identical which is the case as we have cloned the VMs)
