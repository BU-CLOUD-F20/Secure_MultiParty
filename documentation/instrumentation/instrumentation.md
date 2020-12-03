# Instrumentation of MPC Source Code

## Make Changes to Cleanup Build

1. Note about using random in a multithreaded program from `man random`: "The random() function should not be used in multithreaded programs where reproducible behavior is required.  Use random_r(3) for that purpose" --> Determine whether or not this should be modified in the scenario where we are using MPI...
1. For now, I can avoid all the warnings I originally seen when compiling with `-Wall -pedantic` by using `-std=c11 -D_XOPEN_SOURCE=500` as indicated in `man random`
1. Several warnings about potentially uninitialized variables were quieted by initializing a variable. Several others  appear for set but unused variables when `#define DEBUG` isn't set and printing them. Using `(void)<variable>` in the `#else` ifdef clause silences those warnings.
1. Other optimization note: don't forget about setting parallel builds when calling make, this can speed up jobs... e.g. `make all -j8`
1. Where overflow is expected, use `#pragma GCC diagnostic ignored "-Woverflow"` to silence the warning.
1. Running tests.sh everything seems to be working as expected (though I did not change how the tests were being run...). When looking at the experiments, just single tests are run to see if things are working at a glance. A number of experiments don't seem to be running and may require further inspection...

```
# Output from checking tests
pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/tests$ make all -j8
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-conversion test_conversion.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-primitives test_primitives.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-rsz test_rsz.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-share test_sharing.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-select test_select.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-rca test_rca.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-equality test_binary_equality.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-relational test_relational.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-group test_group_by.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-distinct test_distinct.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-sort test_sort.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-inequality test_binary_inequality.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-join test_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-in test_in.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-arithmetic-to-binary test_arithmetic_to_binary.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-ageq test_adjacent_geq.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q1 test_q1.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q2 test_q2.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q3 test_q3.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/tests$ ./tests.sh 
rm -f test-conversion test-primitives test-rsz test-share test-select test-rca test-equality test-relational test-group test-distinct test-sort test-inequality test-join test-in test-arithmetic-to-binary test-ageq test-group-join test-q1 test-q2 test-q3 *.o *.exec
Running test: test-primitives
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-primitives test_primitives.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST PRIMITIVES: OK.
TEST PRIMITIVES: OK.
TEST PRIMITIVES: OK.
Running test: test-share
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-share test_sharing.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST SHARING: OK.
TEST SHARING: OK.
TEST SHARING: OK.
Running test: test-rsz
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-rsz test_rsz.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST GET_NEXT_RB(): OK.
TEST GET_NEXT_RB_ARRAY(): OK.
Running test: test-equality
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-equality test_binary_equality.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST EQ_B(): OK.
TEST EQ_B_ARRAY(): OK.
Running test: test-inequality
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-inequality test_binary_inequality.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST GREATER(): OK.
TEST GEQ(): OK.
TEST GEQ_BATCH(): OK.
TEST GREATER_BATCH(): OK.
Running test: test-rca
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-rca test_rca.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST RIPPLE CARRY ADDER: OK.
Running test: test-join
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-join test_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST JOIN: OK.
TEST BATCH JOIN: OK.
Running test: test-select
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-select test_select.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST SELECT: OK.
Running test: test-relational
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-relational test_relational.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
RELATIONAL (SELECTIONS): OK.
TEST RELATIONAL: OK.
Running test: test-conversion
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-conversion test_conversion.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST B2A CONVERSION (SINGLE-BIT): OK.
Running test: test-sort
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-sort test_sort.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST CMP_SWAP(): OK.
TEST CMP_SWAP_G(): OK.
TEST SORT: OK.
TEST BATCH SORT: OK.
TEST BATCH SORT (2 ATTRIBUTES): OK.
TEST BATCH SORT (3 ATTRIBUTES): OK.
Running test: test-distinct
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-distinct test_distinct.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST DISTINCT: OK.
TEST DISTINCT (BATCH): OK.
Running test: test-group
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-group test_group_by.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST GROUP_BY: OK.
TEST GROUP_BY (MICRO): OK.
Running test: test-in
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-in test_in.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST IN: OK.
Running test: test-arithmetic-to-binary
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-arithmetic-to-binary test_arithmetic_to_binary.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
TEST A2B CONVERSION: OK.
Running test: test-ageq
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-ageq test_adjacent_geq.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST ADJACENT GEQ: OK.
Running test: test-q1
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q1 test_q1.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST Q1: OK.
Running test: test-q2
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q2 test_q2.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST Q2: OK.
Running test: test-q3
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-q3 test_q3.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST Q3: OK.
Running test: test-group-join
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o test-group-join test_group_by_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
TEST GROUP-BY-JOIN: OK.
```

1. After some tweaking, I've found settings that make it possible to run most of the experiments successfully except for exp-semi-join and exp-group-by-join-naive some working parameters are set in experiments.sh

```
pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/experiments$ ./experiments.sh 
rm -f exp-equality exp-cmp-swap exp-exchange exp-reveal exp-greater exp-rca exp-distinct exp-join exp-semi-join exp-order-by exp-group-by exp-group-by-baseline exp-q1 exp-q1-baseline exp-q2 exp-q2-baseline exp-q3 exp-q3-baseline exp-join-distinct-naive exp-join-distinct-opt exp-group-by-join-naive exp-group-by-join-opt exp-select-distinct-opt exp-select-distinct-naive exp-geq-join *.o *.exec
Running experiment: exp-equality
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-equality exp_equality.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
SYNC    256     0.001
ASYNC   256     0.001
ASYNC-ARRAY     256     0.001
ASYNC-INTER     256     0.001
Running experiment: exp-exchange
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-exchange exp_exchange.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
BATCHED 256     0.00000
SYNC    256     0.00014
ASYNC   256     0.00013
Running experiment: exp-reveal
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-reveal exp_reveal.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
SYNC    256     0.000
ASYNC   256     0.000
Running experiment: exp-greater
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-greater exp_greater.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
256     0.005
Running experiment: exp-rca
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-rca exp_rca.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
256     0.004
Running experiment: exp-cmp-swap
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-cmp-swap exp_comp_swap.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c -lsodium -lm                        
256     CMP-SWAP-BATCH  256     0.009
Running experiment: exp-distinct
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-distinct exp_distinct.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
1       DISTINCT-BATCH  256     0.001
Running experiment: exp-group-by
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-group-by exp_group_by.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     GROUP-BY        0.002
Running experiment: exp-group-by-baseline
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-group-by-baseline exp_group_by_baseline.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     GROUP-BY-BASELINE       0.010
Running experiment: exp-q2
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q2 exp_q2.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
Order-by.
1st selection.
Distict.
2nd Order-by.
        Q2      256     0.553
Running experiment: exp-q2-baseline
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q2-baseline exp_q2_baseline.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
        Q2-baseline     256     230.182
Running experiment: exp-select-distinct-opt
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-select-distinct-opt exp_select_distinct_opt.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     OPT select-distinct     0.232
Running experiment: exp-select-distinct-naive
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-select-distinct-naive exp_select_distinct_naive.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     NAIVE select-distinct   0.102
Running experiment: exp-join
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-join exp_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
1       JOIN-BATCH      256     0.282
Running experiment: exp-semi-join
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-semi-join exp_semi_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
1       IN-BATCH        256     256     0.302
[Lux:09283] *** Process received signal ***
[Lux:09283] Signal: Aborted (6)
[Lux:09283] Signal code:  (-6)
[Lux:09284] *** Process received signal ***
[Lux:09284] Signal: Aborted (6)
[Lux:09284] Signal code:  (-6)
[Lux:09285] *** Process received signal ***
[Lux:09285] Signal: Aborted (6)
[Lux:09285] Signal code:  (-6)
exp-semi-join: malloc.c:4033: _int_malloc: Assertion `(unsigned long) (size) >= (unsigned long) (nb)' failed.
corrupted size vs. prev_size
corrupted size vs. prev_size

^CRunning experiment: exp-q1
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q1 exp_q1.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
        Q1      256     256     0.512
Running experiment: exp-q1-baseline
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q1-baseline exp_q1_baseline.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
        Q1-BASELINE     256     256     0.516
Running experiment: exp-q3-baseline
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q3-baseline exp_q3_baseline.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
6       Q3-BASELINE     256     256     231.779
Running experiment: exp-join-distinct-naive
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-join-distinct-naive exp_join_distinct_naive.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     NAIVE JOIN-DISTINCT     106.211
Running experiment: exp-join-distinct-opt
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-join-distinct-opt exp_join_distinct_opt.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     OPT JOIN-DISTINCT       0.760
Running experiment: exp-group-by-join-naive
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-group-by-join-naive exp_group_by_join_naive.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
[Lux:09483] *** Process received signal ***
[Lux:09483] Signal: Segmentation fault (11)
[Lux:09483] Signal code: Invalid permissions (2)
[Lux:09483] Failing at address: 0x7fedd40d3000
[Lux:09483] [ 0] /lib/x86_64-linux-gnu/libc.so.6(+0x3f040)[0x7feddfc3c040]
[Lux:09483] [ 1] exp-group-by-join-naive(+0xa778)[0x5563b1ba0778]
[Lux:09483] [ 2] exp-group-by-join-naive(+0x10e35)[0x5563b1ba6e35]
[Lux:09483] [ 3] exp-group-by-join-naive(+0x1825)[0x5563b1b97825]
[Lux:09483] [ 4] /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xe7)[0x7feddfc1ebf7]
[Lux:09483] [ 5] exp-group-by-join-naive(+0x1c9a)[0x5563b1b97c9a]
[Lux:09483] *** End of error message ***
--------------------------------------------------------------------------
mpirun noticed that process rank 2 with PID 0 on node Lux exited on signal 11 (Segmentation fault).
--------------------------------------------------------------------------
Running experiment: exp-geq-join
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-geq-join exp_geq_join.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
[0] ROWS1: 256   ROWS2: 256
Done with initialization.
[2] ROWS1: 256   ROWS2: 256
[1] ROWS1: 256   ROWS2: 256
Done with share generation.
Rank [2]: seeds exchnaged.
Rank [2]: tables allocated... Starting computation.
Rank [1]: seeds exchnaged.
Rank [1]: tables allocated... Starting computation.
Rank [0]: seeds exchnaged.
Rank [0]: tables allocated... Starting computation.
Rank [1]: Done.
Rank [0]: Done.
Rank [2]: Done.
EXP-GEQ-JOIN    256     256     1.508
Running experiment: exp-order-by
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-order-by exp_order_by.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
3       ORDER-BY        256     0.564
Running experiment: exp-q3
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-q3 exp_q3.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
6       Q3-BATCH        256     256     256     2.529
Running experiment: exp-group-by-join-opt
mpicc -std=c11 -D_XOPEN_SOURCE=500 -O3 -Wall -pedantic      -o exp-group-by-join-opt exp_group_by_join_opt.c ../src/comm.c ../src/party.c ../src/primitives.c ../src/sharing.c ../src/utils.c ../src/relational.c -lsodium -lm                        
256     OPT group-by-join       0.392
```

## Instrumentation for exp-exchange
1. Replaced the gettimeofday with clock_gettime and using CLOCK_MONOTONIC as it is unaffected by discontinyous jumps in system time.
1. Added in additional measurement of some setup setps in the experiment (it turns out that generating the random values takes a significant portion of the total time).
1. The function now takes more than a single input value instead taking instead `[INPUT_SIZE_START] [STEP_SIZE] [NUM_STEPS] [NUM_ITER]` for example: `mpirun --host localhost,<remote1>,<remote2> -np 3 exp-exchange 100 10 6 3`
1. The output is currently printed both to the screen and by the rank 0 node to a csv file. The csv file is named such that it containes the date and timestamp so as to distinguish between multiple test runs. Note: make sure that the program is able tp write to the current directory! Also, potentially modify so that printing to scree/file can be independendtly enabled.
