# Steps to create a VM on the MOC
*Follow these sections and steps in order!*

## Logging In
1. Based on the [shared Google Doc](https://docs.google.com/document/d/1LD2t9uXyIkzlyaQu_MJ2FhyZKYw6uAb1sBL0RFeV28s/edit) and the MOC OpenStack dashboard tutorial on [this](https://docs.massopen.cloud/en/latest/openstack/OpenStack-Tutorial-Index.html) page:
  1. Access the OpenStack Dashboard by navigating to https://kaizen.massopen.cloud/
  1. Select "Institution Account" and "Connect"

      ![openstack_login1](/Images/openstack_login1.png)

  1. Select "University Logins"

      ![openstack_login2](/Images/openstack_login2.png)

  1. Enter BU standard credentials at the prompt

      ![openstack_login3](/Images/openstack_login3.png)

  1. If you encounter the following screen, and are not able to login using BU credentials, use "Google login"

      ![openstack_login5](/Images/openstack_login5.png)

      ![openstack_login6](/Images/openstack_login6.png)

  1. The OpenStack dashboard should now be visible

      ![openstack_login4](/Images/openstack_login4.png)

1. Once the dashboard is reached an overview is available [here](https://docs.massopen.cloud/en/latest/openstack/Dashboard-Overview.html)

## Creating a Network
1. The next step should be to [create a private network for our project/test](https://docs.massopen.cloud/en/latest/openstack/Set-up-a-Private-Network.html)
  1. Viewing the network topology shows what networks are available to all projects (There is more available than in the MOC screenshot guide)

      ![network1](/Images/network1.png)

  1. Create a new network using the button on the right side of the screen leaving the defaults

      ![network2](/Images/network2.png)

  1. On the Subnet tab picking IP addresses that fall within the ranges for private networks
      1. 10.0.0.0/8
      1. 172.16.0.0/12
      1. 192.168.0.0/16

      ![network3](/Images/network3.png)

  1. on the Subnet Details tab make sure that DHCP is selected and that a DNS server is configured
      1. 8.8.8.8 and 8.8.4.4 are Google DNS servers
      1. 1.1.1.1 and 1.0.0.1 are Cloudflare DNS servers
      1. Many other options exist...

      ![network4](/Images/network4.png)

  1. After selecting create, the new network appears alongside the others in the topology display

      ![network5](/Images/network5.png)

## Creating a Router
1. In order to connect the previously created network to the outside internet, [a router is needed](https://docs.massopen.cloud/en/latest/openstack/Create-a-Router.html).
  1. Create a router using the button on the right side of the Network Topology screen leaving the defaults

      ![network2](/Images/network2.png)

  1. After naming the router, select an external network (Rather than "public" as indicated in the MOC guide this seems to be named "external")

      ![network6](/Images/network6.png)

  1. After selecting create, the router will now appear but only connected to the external/public network

      ![network7](/Images/network7.png)

  1. Moving away from the Network Topology page to the Router page we can click on the router we just created

      ![network8](/Images/network8.png)

  1. Selecting the Interfaces tab we can use the Add Interface button the on the right hand side of the page.
      1. On the resulting Add Interface window, the subnet we previously created can be selected

          ![network9](/Images/network9.png)

          ![network10](/Images/network10.png)

  1. At this point, the Network Topology page should show the router connecting our subnet and the external world

      ![network11](/Images/network11.png)

## Security Groups
1. Prior to creating a VM, [security settings](https://docs.massopen.cloud/en/latest/openstack/Security-Groups.html) need to be configured in order to use ssh.
  1. Note, the MOC guide is out of date, Instead of Compute -> Access and Security navigate to Network -> Security Groups (Note: There is a "default" group with some preset firewall rules)

      ![security1](/Images/security1.png)

  1. Let's create a new group that will only allow incoming SSH connections (In the future we may want other rules in order to install software or perform other communications...)
      1. Using the Create Security Group button on the right side of the page select a new name for the group

          ![security2](/Images/security2.png)

      1. Once the new security group appears the Manage Rules button on the same row can be used to configure the desired behavior (Using the Add Rule button on the subsequent page).

          ![security3](/Images/security3.png)

          ![security4](/Images/security4.png)

  1. The new rule appears though we will need to create a VM in order to test it.

      ![security5](/Images/security5.png)

## Adding a Key Pair (for SSH)
1. In order to access a default VM (which does not have password authentication enabled) [it will be necessary to import an SSH key pair](https://docs.massopen.cloud/en/latest/openstack/Create-a-Key-Pair.html). This can be achieved from the Compute -> Key Pairs page

   ![key1](/Images/key1.png)

  1. If you don't have an SSH key pair available, it is necessary to create on first. Follow the example in the MOC guide to create on locally
    ```
    $ cd ~/.ssh
    $ ssh-keygen -t rsa -f ~/.ssh/cloud.key -C "label_your_key"
    ```
      ![key2](/Images/key2.png)

  1. Carefully follow the suggestions on the key generation page before uploading the public key to the MOC

      ![key3](/Images/key3.png)

  1. After uploading the key should exist on the Key Pairs page

      ![key4](/Images/key4.png)

  1. Remember to add the key to your ssh-agent in order to be able to access your VM and to use agent forwarding if attempting to access VMs over multiple hops!
      1. To add the key to ssh-agent do as indicated by the MOC guide:
      ```
      $ cd ~/.ssh
      $ ssh-add cloud.pem
      ```
      1. Note: you may need to launch the ssh-agent first i.e. ``eval ssh-agent``

## Launching a VM
1. We will use a base public image and [follow the MOC guide](https://docs.massopen.cloud/en/latest/openstack/Launch-a-VM.html) in order to launch a VM.
  1. Project -> Compute -> Images contains public options (As John mentioned using Ubuntu previously I will use that for now (though there shouldn't be any particular preference between Linux distributions))

      ![vm1](/Images/vm1.png)

  1. Select "Launch" next to the base image of choice (Ubuntu20.04LTS is used here) then review all the pages before confirming the launch.

      ![vm2](/Images/vm2.png)

      ![vm3](/Images/vm3.png)

      ![vm4](/Images/vm4.png)

      ![vm5](/Images/vm5.png)

      ![vm6](/Images/vm6.png)

      ![vm7](/Images/vm7.png)

  1. Once all the settings are specified, launch the VM and navigate to Compute ->Instances

      ![vm8](/Images/vm8.png)
      *In progress...*

      ![vm9](/Images/vm9.png)
      *Successfully launched!*

## Assigning a Floating IP
1. Attaching a floating IP will make it possible to use ssh to access the VM. [Follow the MOC guide.](https://docs.massopen.cloud/en/latest/openstack/Assign-a-Floating-IP.html)
1. Navigate to Compute -> Instances and using the dropdown menu select "Associate Floating IP"

    ![ip1](/Images/ip1.png)

  1. If no IP is allocated, use the plus sign to allocate a new one! (We only appear to get two so we may need to pass through a gateway VM to any other VMs we create)
  1. See the following images for the steps taken:

      ![ip2](/Images/ip2.png)

      ![ip3](/Images/ip3.png)

      ![ip4](/Images/ip4.png)

      ![ip5](/Images/ip5.png)

  1. It is possible to disassociate the IP and move it to another VM or to release it back to the MOC pool entirely (See the MOC guide if help is needed to accomplish this)

## Connecting to a VM over SSH
1. If all the previous steps were completed successfully it should be possible to access a VM on the cloud via SSH now. See the steps in [this MOC guide.](https://docs.massopen.cloud/en/latest/openstack/SSH-to-Cloud-VM.html)
  1. As the Ubuntu base image was used, the default username will be 'ubuntu'
  1. Note, I had to explicitly specify my ssh key file in order to be able to log into the VM

      ![ssh1](/Images/ssh1.png)
      *Initial error*

      ![ssh2](/Images/ssh2.png)
      *Successful login*

  1. Once logged-in I made sure to change the password to randomly generated one (in case I need access from the web-console in the future). This was accomplished using `sudo passwd ubuntu`
  1. Next I updated the VM (Using apt for Ubuntu) This may take a little while...
  ```
  sudo apt update
  sudo apt upgrade
  ```

## Next Steps...
1. In order to confirm success for this task, I ran "hello world on the VM"
  1. First I installed developer tools on the VM (Will we want to be doing our builds in the cloud?) Note: If we will be doing builds in the cloud, maybe we should do that on one VM and then move the programs to other VMs so that we can keep them lighter weight?
  `sudo apt install build-essential`
  1. Then I wrote a "hello world" program in C, built, and then executed the program.

      ![ssh3](/Images/ssh3.png)

1. In order for other team members to be able to accomplish this task I will now add additional users to the VM which they will be able to access.
  1. To be continued... [following this part of the MOC guide](https://docs.massopen.cloud/en/latest/openstack/SSH-to-Cloud-VM.html)
  1. In order to create new users (following MOC guide with some additions and pwolfe as an example):
  ```
  sudo su
  useradd -m pwolfe
  passwd pwolfe
  usermod -aG sudo pwolfe
  # Change user
  su pwolfe
  # copy authorized ssh key into .ssh/authorized_key
  mkdir /home/pwolfe/.ssh
  touch /home/pwolfe/.ssh/authorized_key
  nano /home/pwolfe/.ssh/authorized_key
  # Now enter the key...
  # Change default user shell
  sudo usermod --shell /bin/bash pwolfe
  # Alternately use chsh interactively
  ```
  1. Once the authorized_key is configured for the user, they can attempt to ssh into the VM.
  1. Note, if the machine needs to be rebooted you can always use `sudo reboot now`
