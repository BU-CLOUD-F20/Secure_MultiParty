# Single-bare-metal Node Setup

0. For more detailed information, follow docs on *[cloudlab](http://docs.cloudlab.us/getting-started.html)*.


1. Create an cloudlab account with public key and wait for official approval. For team members, select "join existing project" and input "MPCproject" when creating an account.


2. Click "Experiment" and then "Start Experiement".


3. Select 'Single-bare-metal' node on profile page.

![clab](/Images/cdoc3.png)

4. Comparing with choosing "OpenStack" profile, "Single-bare-metal" does not requires users to parameterize. See *[here](http://docs.cloudlab.us/hardware.html)* for different hardware selection. Cloudlab Utah cluster was chosen for this experiment.

5. After the profile is provisioned, the experiment is ready to go.

![clab](/Images/cdoc2.png)

6. Connecting shell with ssh command using terminal, with your private key.

![clab](/Images/cdoc1.png)

7. Create a simple C helloworld program and edit it with vi editor. And then run it with gcc complier. (Avoid writing code directly on vm, latency is high when typing.)

![clab](/Images/cdoc4.png)

8. Running Mpi helloworld on a single-bare-metal node. Reference on *[MPI tutorial](https://mpitutorial.com/tutorials/mpi-hello-world/)*

  ```shell
  sudo apt install libopenmpi-dev
  ```
  Before running mpirun command, make sure the following pacakge is installed.
  ```shell
  sudo apt install openmpi-bin
  ```

 ![clab](/Images/cdoc5.png)
