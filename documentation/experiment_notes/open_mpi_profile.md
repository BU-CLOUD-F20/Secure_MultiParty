# Profiling Tools for OpenMPI
*WIP*

## Initial Exploration
1. Testing MPC code on a personal CentOS 7 machine in the CAAD lab at BU (prior to committing to installing on the VMs)
    ```
    sudo yum install libsodium-devel openmpi-devel openmpi3-devel
    # (I probably didn't need to install openmpi3-devel but I did...)
    ```
1. I discovered that module was installed on CentOS 7 but needed to be made available using:
`source /etc/profile.d/modules.sh` Then I was able to load OpenMPI using `module load mpi`
1. After that I could make the MPC software though I did need to add -std=c99 to the mpicc line in both Makefiles
1. From there I could run the `./tests.sh` in the tests folder and the exp-exchange operation under experiments using the same command as previously:
    ```
    [pwolfe@dhcp-acadmin-128-197-176-103 experiments]$ mpirun -np 3 exp-exchange 1000
    [1602539565.163812] [dhcp-acadmin-128-197-176-103:13092:0]            sys.c:618  UCX  ERROR shmget(size=2097152 flags=0xfb0) for mm_recv_desc failed: Operation not permitted, please check shared memory limits by 'ipcs -l'
    [1602539565.163849] [dhcp-acadmin-128-197-176-103:13093:0]            sys.c:618  UCX  ERROR shmget(size=2097152 flags=0xfb0) for mm_recv_desc failed: Operation not permitted, please check shared memory limits by 'ipcs -l'
    [1602539565.168768] [dhcp-acadmin-128-197-176-103:13091:0]            sys.c:618  UCX  ERROR shmget(size=2097152 flags=0xfb0) for mm_recv_desc failed: Operation not permitted, please check shared memory limits by 'ipcs -l'
    BATCHED 1000    0.00004
    SYNC    1000    0.00019
    ASYNC   1000    0.00021
    ```
There were some problems however... Following the suggestion:
    ```
    [pwolfe@dhcp-acadmin-128-197-176-103 experiments]$ ipcs -l

    ------ Messages Limits --------
    max queues system wide = 32000
    max size of message (bytes) = 8192
    default max size of queue (bytes) = 16384

    ------ Shared Memory Limits --------
    max number of segments = 4096
    max seg size (kbytes) = 18014398509465599
    max total shared memory (kbytes) = 18014398442373116
    min seg size (bytes) = 1

    ------ Semaphore Limits --------
    max number of arrays = 128
    max semaphores per array = 250
    max semaphores system wide = 32000
    max ops per semop call = 32
    semaphore max value = 32767
    ```
This could be resolved with the following command:
    ```
    # https://stackoverflow.com/questions/45910849/shmget-operation-not-permitted
    sudo setcap cap_ipc_lock=ep exp-exchange
    ```
    Which produces the following output:
    ```
    [pwolfe@dhcp-acadmin-128-197-176-103 experiments]$ mpirun -np 3 exp-exchange 1000
    BATCHED 1000    0.00004
    SYNC    1000    0.00021
    ASYNC   1000    0.00022
    ```
1. At this point we can work on our main goal of employing some profiling tools...
First I will test [Score-P](https://www.vi-hps.org/projects/score-p/)
On centos 7 I can run `sudo yum install scorep`
1. Prefixing mpicc with scorep in the makefile resulted in an error when building, maybe I need the scorep specific openmpi files? Trying `sudo yum install scorep-openmpi scorep-openmpi3`
That made some progress... (Specifically the scorep-openmpi3)
Then I needed to `sudo yum install scorep-openmpi3-config` after which the build finally completes...
1. Now to try and capture some data... Running the exp-exchange build with scorep results in an output file.
    ![scorep1](/Images/scorep1.png)
1. As Vampir only appears to have paid versions I've installed Scalasca to try to make a preliminary examination of the trace captured. (Also note [this](http://scorepci.pages.jsc.fz-juelich.de/scorep-pipelines/docs/scorep-6.0/html/index.html) page for how some of the profiling tools work) I installed it just by using `sudo apt install scalasca`
1. After calling scalasca on one of the previously saved files `scalasca -examine scorep-20201012_1828_34604691544698723/` I was able to get the following view:
    ![scorep2](/Images/scorep2.png)
1. Going forward I think that it should be possible to generate the scorep files on the VMs and then examine them offline on another machine to try and gain some insights into where performance is going.
