# Docker setup notes

*Local testing before deploying to OpenShift*

*The testing as performed was using WSL2 on Windows 10*

*This is after discovering Hyper-V is no longer needed to back Docker on Windows*

Following the example here:
https://docs.docker.com/engine/reference/commandline/exec/#examples

---

## Attempting an Interactive Setup
*If this works I can create a dockerfile with the known good steps*

1. Launch a container...
    ```
    # docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
    docker run --name ubuntu_dev --rm -i -t ubuntu:20.04 bash
    ```
    --name what to call the container
    --rm remove container on exit
    -i interactive, keep STDIN open
    -t allow a psuedo-TTY
    -d detached mode

1. Okay, I learned the following: Start the container in detached mode, avoid the -rm so that I can reconnect. If I don't start in detached mode used `docker start` to resume the connection... (start, stop, rm can be used to manage the container)
    ```
    # Launch like this instead:
    container1=`docker run --name ubuntu_dev -d -i -t ubuntu:20.04 bash`
    echo $container1
    docker attach $container1
    # In container
    apt update && apt install -y make gcc libopenmpi-dev openmpi-bin openmpi-common openmpi-doc libsodium23 libsodium-dev

    # something was interactive here... avoid docs next time?
    # mpi complains about running as root
    # Look into changing away from root user (the repo below might have a fix)
    # Temporarily overriding to test... and it works...
    mpirun --allow-run-as-root -np 3 hostname

    # To Do:
    # can we build with mpi?
    # can we use mpi across multiple containers?
    # can we change to not running as root?
    ```

1. Note: [This repo](https://github.com/oweidner/docker.openmpi) seems to be what we are sort of trying to get to with docker...

1. Now lets try building and testing some MPC code in a single container...
    ```
    # Creating a spot into which to copy the source code...
    # Still using the docker tty
    mkdir /home/mpc
    cd /home/mpc

    # Exit tty now, copy files in from the host side
    docker cp /mnt/d/Documents/BU\ Cloud/repos/ccproject/src $container1:/home/m
    pc/
    docker start $container1
    docker attach $container1
    cd /home/mpc
    ls

    # The files were successfully copied, so now to repeat with the other folders...
    exit
    # Now back on the host
    docker cp /mnt/d/Documents/BU\ Cloud/repos/ccproject/tests $container1:/home/m
    pc/
    docker cp /mnt/d/Documents/BU\ Cloud/repos/ccproject/experiments $container1:/home/m
    pc/
    # Return to container
    docker start $container1
    docker attach $container1
    cd /home/mpc/experiments

    # Now to try building...
    make clean
    make exp-exchange

    # Now to try running...
    root@bb82ee92a680:/home/mpc/experiments# mpirun --allow-run-as-root -np 3 exp-exchange 1000
    [bb82ee92a680:00045] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00045] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00046] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00046] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00044] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00045] Read -1, expected 8000, errno = 1
    [bb82ee92a680:00046] Read -1, expected 8000, errno = 1
    BATCHED 1000    0.00013
    SYNC    1000    0.00105
    ASYNC   1000    0.00055

    # It ran but there is some odd warning/error?

    # One way to check the size:
    docker ps -a -s -f "id=$container1"
    # Alternately
    docker system df --verbose
    # Current size of container is ~500MB max
    # Need to check original size and also try with just the runtimes for openmpi and libsodium installed...
    ```

## Continuing work with local Docker instances...

1. To resume the last docker instance it is possible to obtain the IMAGE ID and use that to start the instance
    ```
    container1=`docker ps -q -l`
    docker start -a -i $container1
    # or alternately in one line as follows...
    docker start -a -i `docker ps -q -l`
    ```
1. I navigated to /home/mpc/tests and then built all of the verification programs
    ```
    # Inside the container
    cd /home/mpc/tests
    make all
    #
    ```
1. I have to make sure to modify the tests.sh script since I still haven't modified the docker instance to be running as a non-root user... I include the flag `--allow-run-as-root` for the `mpirun` macro
1. Now, running the tests succeeds (which was expected as exp-exchange functioned properly yesterday too).

## Some Additional Discoveries

1. While starting down the path of creating a non-root user in docker and seeking to have that non-root user evaluate the docker `CMD` in the Dockerfile, I determined that there was a specific discussion about OpenMPI and docker that eventually came to the agreement of having two environment flags that could be set to specify running as a root user (as is typical for Docker).
1. Including the following makes it possible to run as openmpi as root without having to pass a command-line flag:
    ```
    ENV OMPI_ALLOW_RUN_AS_ROOT=1
    ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
    ```
1. One remaining observation, despite appearing to run correctly, for certain message sizes passed to exp-exchange, warnings are produced though the program completes running.
1. Starting from the Dockerfile which can be built using `docker build -t mpc` when in the scripts subdirectory I can launch an interactive instance of the container by calling: `docker run --name mpc -it mpc /bin/bash`. Should I ever close the container, I can start it `docker start mpc` and then attach to it `docker attach mpc`. Once attached, I can do the following to demonstrate the issue:
    ```
    mpirun -np 3 exp-exchange 1000
    # which produces the following:
    root@ebd1c7f24dfe:~/experiments#
    [ebd1c7f24dfe:00046] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00046] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00047] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00047] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00045] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00047] Read -1, expected 8000, errno = 1
    [ebd1c7f24dfe:00046] Read -1, expected 8000, errno = 1
    BATCHED 1000    0.00005
    SYNC    1000    0.00047
    ASYNC   1000    0.00042
    ```
1. By manually installing gdb and an editor in the interactive instance of this container, I can try to debug and determine where these messages are coming from. One interesting note is that they seem to only occur once the message size (in the above example 1000) is beyone a certain size. 500 did not cause these messages to appear for example.
    ```
    apt install gdb nano
    nano env_exchange.c
    # Add some debug statements
    nano Makefile
    # modify to remove -03 and add -g
    make clean
    make exp-exchange
    ```
1. In order to be able to attach to one specific MPI process I inserted the following based on the [OpenMPI debugging page](https://www.open-mpi.org/faq/?category=debugging).
    ```
    # Include rank condition if you only want to connect to one specific thread
    if (rank == 0) {
    volatile int i = 0;
    char hostname[256];
    gethostname(hostname, sizeof(hostname));
    printf("PID %d on %s ready for attach\n", getpid(), hostname);
    fflush(stdout);
    while (0 == i)
        sleep(5);
    }
    ```
1. After launching `mpirun -np 3 exp-exchange 1000 &` I am then greeted by something as follows: `PID 80 on ebd1c7f24dfe ready for attach`
1. I can attach gdb by calling `gdb --pid 80` and then attempt to use `fin` and 'l' until I see that I am back at the level of the sleep call. (I did have some occasions where gdb would hang and I could use `ps` to identify the unterminated mpi calls and use `kill` to end them before trying again... note: it turns out this is if I happen to attach specifically when the program is in linux/poll.c)
1. I can then use `set var i = 7` (or any non-zero number) to make sure I break out of the sleep loop. I also set breakpoints of interest later in exp-exchange at this point.
1. After some exploration, the source of these messages appears to be occurring at the MPI_Send and MPI_Recv in generate_and_share_random_data (producing 4 of the outputs). One come from exchange_rsz_seeds. The final two come from exchange_shares_array. Note: a useful shortcut when using gdb to execute until a certain line is `until #` or `u #`
1. Having determined that one of these messages happens per each MPI_Send MPI_Recv pair, I need to now determine what specifically is causing them to appear but only certain circumstances...
1. I further confirmed that the message appears after MPI_Recv runs (see example below)
    ```
    Thread 1 "exp-exchange" hit Breakpoint 2, generate_and_share_random_data (rank=1, r1s1=0x555ef71c27d0, r1s2=0x555ef71c4720, ROWS=1000)
    at ../src/utils.c:216
    216         MPI_Recv(r1s1, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    (gdb) l
    211         // free temp tables
    212         free(r1);
    213         free(r1s3);
    214       }
    215       else if (rank == 1) { //P2
    216         MPI_Recv(r1s1, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    217         MPI_Recv(r1s2, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    218       }
    219       else { //P3
    220         MPI_Recv(r1s1, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    (gdb) p r1s1
    $4 = (BShare *) 0x555ef71c27d0
    (gdb) p r1s1[0]
    $5 = 0
    (gdb) p ROWS
    $6 = 1000
    (gdb) p MPI_LONG_LONG
    No symbol "MPI_LONG_LONG" in current context.
    (gdb) p SHARE_TAG
    $7 = 193
    (gdb) p MPI_COMM_WORLD
    No symbol "MPI_COMM_WORLD" in current context.
    (gdb) p MPI_STATUS_IGNORE
    No symbol "MPI_STATUS_IGNORE" in current context.
    (gdb) s
    [ebd1c7f24dfe:00323] Read -1, expected 8000, errno = 1
    217         MPI_Recv(r1s2, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    (gdb)
    ```
