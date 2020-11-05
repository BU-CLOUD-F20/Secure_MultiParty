# Summary of steps for Duplicating the Primary VM

*By duplicating the primary VM we can obtain two other identical images which we can use as our three MPC parties*

1. Stop the primary VM and create a snapshot in the OpenStack interface

    ![clone_vm1](/Images/clone_vm1.png)

1. Navigate to Images and launch a new image based on the snapshot going through the following steps:

    ![clone_vm2](/Images/clone_vm2.png)

1. Notice that we can specify a count and OpenStack will create <Instance Name>-# VMs based on our specifications.

    ![clone_vm3](/Images/clone_vm3.png)

1. Select the saved snapshot...

    ![clone_vm4](/Images/clone_vm4.png)

1. Matching resources are selected for now (primary is also an m1.large)

    ![clone_vm5](/Images/clone_vm5.png)

1. Select the same subnet as the primary...

    ![clone_vm6](/Images/clone_vm6.png)

1. Enable SSH...

    ![clone_vm7](/Images/clone_vm7.png)

1. Make sure your SSH key is selected.

    ![clone_vm8](/Images/clone_vm8.png)

1. Launch the Instances then navigate to the Instanced tab to verify successful creation.

    ![clone_vm9](/Images/clone_vm9.png)

1. Also check the Network Topology to see that the VMs are where we expect them to be.

    ![clone_vm10](/Images/clone_vm10.png)

1. Attempt to SSH into the new VMs via the primary using SSH Agent Forwarding

    ![clone_vm11](/Images/clone_vm11.png)
