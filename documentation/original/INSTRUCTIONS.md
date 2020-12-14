# Cloud Computing course project: Benchmarking MPC on MOC

## Dependencies
- Download and install [Libsodium](https://libsodium.gitbook.io/doc/installation). Link with `-lsodium`.
- Download and install [OpenMPI](https://www.open-mpi.org/software/ompi/v4.0/). Compile with `mpicc` and run with `mpirun -np $NUM_PARTIES $PROGRAM`.

## Run tests
- `make tests`

## Run the MPC codebase on a Linux VM
- We used Ubuntu 20.04 Linux distribution to run the codebase on.
- To run the code use the Makefile present in the [experiments](experiments) folder.
- Running the code on OSX:
    - Use the variable `CFLAGS= -03 -Wall -lsodium`
- Running the code on Linux:
    - Use the variables `CFLAGS= -03 -Wall` and `DEP= -lsodium -lm`
    - While running on Linux, the placement of `-lsodium` dependency in the command is very important. **DEP** should be specified as follows:

    `exp-equality:   exp_equality.c $(PRIMITIVES) $(MPI) $(CFLAGS) -o exp-equality exp_equality.c $(PRIMITIVES) $(DEP)`
