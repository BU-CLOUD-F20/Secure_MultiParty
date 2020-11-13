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

## Steps Towards Final Resolution

1. After some additional digging, mostly by looking at the returned value from MPI_Recv, it appeared that the error/warning message was not actually from that command but rather from something internal to OpenMPI.
1. With some searching of the OpenMPI github repo I was able to find a line that matched the structure of the message. See [here](https://github.com/open-mpi/ompi/blob/b66e27d3caaf20cabe379656618191ecdba1469c/opal/mca/btl/sm/btl_sm_get.c#L98).
1. Here's a snippet of output from debugging with GDB that illustrates the lack of direct error message from MPI_Recv
  ```
  $12 = {MPI_SOURCE = 0, MPI_TAG = 193, MPI_ERROR = 0, _cancelled = 0, _ucount = 8000}
  (gdb) p result1
  $13 = 0
  (gdb) p status2
  $14 = {MPI_SOURCE = 0, MPI_TAG = 193, MPI_ERROR = 0, _cancelled = 0, _ucount = 8000}
  (gdb) p result2
  $15 = 0
  (gdb) l
  220       }
  221       else { //P3
  222         result1 = MPI_Recv(r1s1, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, &status1);
  223         result2 = MPI_Recv(r1s2, ROWS, MPI_LONG_LONG, 0, SHARE_TAG, MPI_COMM_WORLD, &status2);
  224       }
  225     }
  (gdb)
  ```
1. A few other issues that were open on github discussed this type of situation. See [here](https://github.com/open-mpi/ompi/issues/3270) and [here](https://www.open-mpi.org/faq/?category=sm).
1. In conclusion, for some reason the use of the "vader" mechanism for zero copy sharing (utilized when running mpi on a single node) was not working in the docker environment. Using a specific flag with mpirun would disable that entirely (though having gone through these efforts now, it would seem that when this zero copy mechanism didn't work, mpi was falling back on a different system).
  ```
  # An example call with the override parameter in question
  mpirun --mca btl_vader_single_copy_mechanism none -np 3 exp-exchange 1000
  # instead of
  mpirun -np 3 exp-exchange 1000
  ```

## Deploying Multiple Docker Containers

1. Working with docker-compose, it was possible to create a *.yml file that describes a topology with three parties using the same Dockerfile that defines all of the dependencies needed to run the MPC code.
1. This did require copying the technique used in [this](https://github.com/oweidner/docker.openmpi/blob/master/Dockerfile) reference project both for the Dockerfile and for the *.yml for docker-compose.
1. Additionally, copying the src, tests, and experiments directories into the scripts folder is needed for the Dockerfile to be able to packages those files into containers. Additionally, based on the repo mentioned in the last step, copying the ssh files from that repo (or regenerating versions locally) is also needed to help enable ssh communication between the nodes. The launch.sh script is not actually used but was part of testing (as is the Dockerfile_NEW, which now is another backup)
1. At this point, all that is needed is to run
  ```
  docker-compose build
  docker-compose up
  # Then connect to party-0: the following line is one way of doing so
  # Some other ideas here: https://stackoverflow.com/questions/36249744/interactive-shell-using-docker-compose
  docker-compose exec party-0 bash
  # Change user from root to mpc
  su mpc
  # Execute an mpirun command
  mpirun --host party-0,party-1,party-2 -np 3 exp-exchange 1000
  ```
1. Note: I upgraded from docker-compose version 2.4 to 3.8 as I didn't appear to need any of the older features. [This page](https://docs.docker.com/compose/compose-file/compose-versioning/) provides information about the different versions and how to upgrade between them. Additional follow-up, I switched back to 3.7 as kompose does not yet have a minor version check in it's latest release (a fix is merged though, presumably for the next release)

## Converting for OpenShift Deployment

1. Follow the instructions [here](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/) or [here](https://kompose.io/getting-started/) to convert the docker-compose into a different format.
1. First, since I'm using Docker Desktop backed by WSL2 on Windows 10, I enable a local Kubernetes single node cluster through the gui.
1. While I can launch OpenShift directly from a docker-compose.yml using kompose, I want to try converting to an intermediate file that I can use with different OpenShift deployments.
  ```
  # Download the most recent release of kompose
  curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-linux-amd64 -o kompose
  # Run kompose command on *.yml file
  kompose convert -f docker-compose.yml
  ```

1. I ran into an issue where docker-compose v3.8 files are not yet supported `FATA Version 3.8 of Docker Compose is not supported. Please use version 1, 2 or 3` (just a missing version check). switching to 3.7 works just as before but I see a different kompose error message: `FATA gateway Additional property gateway is not allowed`. It seems that are more issues related to what features are, or are not supported between the different *.yml file versions. I switched to just version "2" without any sub-version and then using kompose the conversion worked properly.
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts$ ../../kompose convert -f docker-compose.yml
    INFO Network scripts_mpc_net is detected at Source, shall be converted to equivalent NetworkPolicy at Destination
    INFO Network scripts_mpc_net is detected at Source, shall be converted to equivalent NetworkPolicy at Destination
    INFO Network scripts_mpc_net is detected at Source, shall be converted to equivalent NetworkPolicy at Destination
    INFO Kubernetes file "party-0-service.yaml" created
    INFO Kubernetes file "party-1-service.yaml" created
    INFO Kubernetes file "party-2-service.yaml" created
    INFO Kubernetes file "party-0-deployment.yaml" created
    INFO Kubernetes file "scripts_mpc_net-networkpolicy.yaml" created
    INFO Kubernetes file "party-1-deployment.yaml" created
    INFO Kubernetes file "party-2-deployment.yaml" created
    ```

1. Now to try using these resources within Kubernetes: `kubectl apply` (Skipped this for now)

1. For OpenShift I can do something similar with a few extra flags:
  ```
  pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts$ ../../kompose --provider openshift --file docker-compose.yml convert
  INFO OpenShift file "party-0-service.yaml" created
  INFO OpenShift file "party-1-service.yaml" created
  INFO OpenShift file "party-2-service.yaml" created
  INFO OpenShift file "party-0-deploymentconfig.yaml" created
  INFO OpenShift file "party-0-imagestream.yaml" created
  INFO OpenShift file "party-1-deploymentconfig.yaml" created
  INFO OpenShift file "party-1-imagestream.yaml" created
  INFO OpenShift file "party-2-deploymentconfig.yaml" created
  INFO OpenShift file "party-2-imagestream.yaml" created
  ```

1. Now, after logging into the MOC OpenShift website, I used the "Copy Login Command" from the user profile dropdown in the top righthand corner. It looks something like this: `../../openshift/oc-tool/oc login https://k-openshift.osh.massopen.cloud:8443 --token=<TOKEN STRING>` though I modified the location of the oc tool. The result is as follows:
  ```
  Logged into "https://k-openshift.osh.massopen.cloud:8443" as "pwolfe@bu.edu" using the token provided.

  You have one project on this server: "ece-528-secure-multiparty"

  Using project "ece-528-secure-multiparty".
  ```
1. Trying to create a new app from the templates...
  ```
  pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts$ ../../openshift/oc-tool/oc new-app --template=party-0-service.yaml,party-1-s
  ervice.yaml,party-2-service.yaml,party-0-deploymentconfig.yaml,party-1-deploymentconfig.yaml,party-2-deploymentconfig.yaml,party-0-imagest
  ream.yaml,party-1-imagestream.yaml,party-2-imagestream.yaml
  error: unable to locate any templates loaded in accessible projects with name "party-0-service.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-1-service.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-2-service.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-0-deploymentconfig.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-1-deploymentconfig.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-2-deploymentconfig.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-0-imagestream.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-1-imagestream.yaml"
  error: unable to locate any templates loaded in accessible projects with name "party-2-imagestream.yaml"

  The 'oc new-app' command will match arguments to the following types:

    1. Images tagged into image streams in the current project or the 'openshift' project
       - if you don't specify a tag, we'll add ':latest'
    2. Images in the Docker Hub, on remote registries, or on the local Docker engine
    3. Templates in the current project or the 'openshift' project
    4. Git repository URLs or local paths that point to Git repositories

  --allow-missing-images can be used to point to an image that does not exist yet.

  See 'oc new-app -h' for examples.
  ```

1. Trying something different:
  ```
  pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts$ ../../openshift/oc-tool/oc new-app scripts_party-0 scripts_party-1 scripts_party-2
  W1111 11:38:09.945481    3901 newapp.go:479] Could not find an image stream match for "scripts_party-0:latest". Make sure that a Docker image with that tag is available on the node for the deployment to succeed.
  --> Found Docker image e444798 (2 hours old) from  for "scripts_party-0:latest"

      * This image will be deployed in deployment config "scriptsparty-0"
      * Port 22/tcp will be load balanced by service "scriptsparty-0"
        * Other containers can access this service through the hostname "scriptsparty-0"
      * WARNING: Image "scripts_party-0:latest" runs as the 'root' user which may not be permitted by your cluster administrator

  W1111 11:38:09.947527    3901 newapp.go:479] Could not find an image stream match for "scripts_party-1:latest". Make sure that a Docker image with that tag is available on the node for the deployment to succeed.
  --> Found Docker image e444798 (2 hours old) from  for "scripts_party-1:latest"

      * This image will be deployed in deployment config "scriptsparty-1"
      * Port 22/tcp will be load balanced by service "scriptsparty-1"
        * Other containers can access this service through the hostname "scriptsparty-1"
      * WARNING: Image "scripts_party-1:latest" runs as the 'root' user which may not be permitted by your cluster administrator

  W1111 11:38:09.947640    3901 newapp.go:479] Could not find an image stream match for "scripts_party-2:latest". Make sure that a Docker image with that tag is available on the node for the deployment to succeed.
  --> Found Docker image e444798 (2 hours old) from  for "scripts_party-2:latest"

      * This image will be deployed in deployment config "scriptsparty-2"
      * Port 22/tcp will be load balanced by service "scriptsparty-2"
        * Other containers can access this service through the hostname "scriptsparty-2"
      * WARNING: Image "scripts_party-2:latest" runs as the 'root' user which may not be permitted by your cluster administrator

  --> Creating resources ...
      deploymentconfig.apps.openshift.io "scriptsparty-0" created
      deploymentconfig.apps.openshift.io "scriptsparty-1" created
      deploymentconfig.apps.openshift.io "scriptsparty-2" created
      service "scriptsparty-0" created
      service "scriptsparty-1" created
      service "scriptsparty-2" created
  --> Success
      Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
       'oc expose svc/scriptsparty-0'
       'oc expose svc/scriptsparty-1'
       'oc expose svc/scriptsparty-2'
      Run 'oc status' to view your app.
    ```

    Now it appears that OpenShift is in the process of launching my containers? I'll check back in a bit to see if things progress past this stage...
    ![openshift_pending](/Images/openshift_pending.png)
