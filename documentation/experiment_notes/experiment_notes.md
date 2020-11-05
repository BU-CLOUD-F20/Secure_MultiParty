# Experiment Notes

## Reproducing Existing Data Collections

1. Based on the recommendations of our mentors, the critical first data to examine is in regards to the data transferred between mpc parties. In their mpc system paper this is examined at the most fundamental level in their figure 7 plot that demonstrates the time taken to pass messages of different sizes using MPI.
1. In order to explore the impact of different deployment environments (and other settings) on the communication we first aim to recreate these results.
    1. The data was collected by running the "exp-exchange" program under the "experiments" directory. This program relies on MPI for communication and measures total runtime using "gettimeofday" at the beginning and end of execution. Within the program, three separate tests are executed in series, each with their own start and stop times. These tests use "exchange_shares_array", "exchange_shares", and "exchange_shares_async" which respectively transfer all the data arranged in an array (in whichever way is selected by MPI), transfer element by element (while blocking), and element by element (without blocking).
    1. In order to execute this test initially, the VMs created on MOC's OpenStack were employed. This required the configuration described in other documents in this repository (see the documentation/openstack directory) and ssh has to be configured to use agent forwarding (see ssh_notes.md). All tests are then launched from the primary VM.
    1. Once on the primary VM, a clone of the codebase repository is located under "/mpc_shared".
        ```
        # Navigate to the directory containing the experiment:
        cd /mpc_shared/ccproject/experiments
        # Using MPI with the appropriate IP addresses specified, run the test
        # Note: exp-exchange takes a message size parameter
        mpirun --host localhost,192.168.100.7,192.168.100.18 -np 3 exp-exchange 1000
        ```
    1. The data is printed to the terminal though it could be redirected to a file. In initial testing it was copied to a *.txt file and subsequently saved to the team Google Drive experiment data folder. A simple initial plot of results appears similar to the plots presented in the mpc system paper which encourages further testing using this method.

        ![original_results](/Images/performance_of_oblivious_primitives.png)
        *Original Results*

        ![new_initial_results](/Images/new_initial_results.png)
        *New Initial Results*

    1. Some observations based on this test and data analysis (in no particular order):
        1. It is very simple to download a plot from Google Sheets using the triple dot menu that appears in the top right corner of the figure in question (when it is clicked on)
        1. The processor speed is not currently accounted for so there is the possibility of a different node being provisioned resulting in performance changes, it would be worth using the clock speed of the processor to measure "operations" performed in addition to raw time. Using the information available in the VMs under /proc/cpuinfo and /proc/meminfo as well as details of the configuration on OpenStack we note that the four virtual processors assigned to the primary VM were from an Intel(R) Xeon(R) CPU E5-2660 v2 @ 2.20GHz and the amount of memory and disk storage were 8Gb and 10Gb respectively (as configured in OpenStack).
        1. All the measurements are performed from the perspective of the primary VM. This is fine for now but we may want to look at how the other VMs are experiencing communication.
        1. In the mpc system paper, the operations tested in figure 7b are equality, inequality, and addition (when assessing total time). These have not yet been tested as the mentors emphasized close examination of the exchange operation. We may return to these once we have sufficiently explored exchange.
        1. We only ran the initial tests from size 10e3 to 10e6 though the tests in the paper range from 10e3 to 10e8. We will return and collect further data to complete the recreation.
        1. The data point for 10e3 for batched exchange resulted in too fast a result so the precision should be increased when timing (so there isn't a 0 data point).
        1. Multiple testruns should be averaged or have the top runs selected as a larger pool of results will tamp down any noise in the data.

## Taking the Tests Further...

1. Note for those performing testing with MPI on a single host running Windows 10 and WSL (version 1). It may be necessary to change the ptrace_scope to prevent MPI from complaining. As described in [this](https://github.com/microsoft/WSL/issues/3397) thread use `sudo su` then `echo 0 > /proc/sys/kernel/yama/ptrace_scope` if the following warning message is seen:
    ```
    WARNING: Linux kernel CMA support was requested via the
    btl_vader_single_copy_mechanism MCA variable, but CMA support is
    not available due to restrictive ptrace settings.

    The vader shared memory BTL will fall back on another single-copy
    mechanism if one is available. This may result in lower performance.
    ```
1. To increase the precision provided when running the tests modify the print statement in exp-exchange (for each of the three tests). Testing on a single host might be interesting as a baseline with which to compare communication between multiple VMs...
1. I tested on my local machine and the trends are as expected (see plot below). This test should be replicated on as single VM and then across multiple VMs (as the first test was)

    ![wsl_initial_results](/Images/wsl_initial_results.png)

1. An interesting observation made was that the memory variation while the tests were executing. When running locally, there was initially primarily a use of RAM by the main process and then later on all of the processes had a similar memory footprint. This should be monitored more closely in the future to better understand the cause of this behavior.

    ![wsl_resource_use1](/Images/wsl_resource_use1.png)

    ![wsl_resource_use2](/Images/wsl_resource_use2.png)

## Replicating Results on VMs (More Completely)

1. After making the small change to precision the tests were run on the VMs again. The tests were run manually 5 times each for sizes 10e3 to 10e6 and two 10e7 tests were run as the test duration was ~20 minutes. No 10e8 tests were run at this time though the trend is expected to continue. Once the tests are scripted larger sizes can be run overtime or on a longer time period without manual interaction. Below is the plot of the results obtained (with a best fit line)

    ![new_initial_results2](/Images/new_initial_results2.png)

    Interestingly, when looking at the data, while the async MPI operations appear to more often show slightly better performance than the sync MPI operations, that is not always the case. Further testing will be needed to eliminate possible sources of noise when running on VMs on the MOC OpenStack.
    ![new_initial_results2_data](/Images/new_initial_results2_data.png)
