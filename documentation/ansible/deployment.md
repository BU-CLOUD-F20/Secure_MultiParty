# Deployment Consolidation

## Ansible
1. Starting from the Ansible documentation located [here](https://docs.ansible.com/ansible/latest) I am following the steps intended for installing on Ubuntu (as I am using an Ubuntu 18.04 WSL2 instance on Windows 10)
1.  I want to use python3 so I will perform the [following](https://docs.ansible.com/ansible/latest/reference_appendices/python_3_support.html):
    ```
    pip3 install ansible
    pip3 install argcomplete

    ```
1. Now that I have ansible available locally, I will follow the basic introductions steps to create a test playbook (and other necessary setup). See [here](https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html).
1. Create `/etc/ansible/hosts` ans specify IP addresses or Fully Qualified Domain Names (FQDNs). Example shown below, add the ip addresses, fqdn, ports, etc...
    ```
    # PF Initial Hosts Test
    [caad]
    caad-pf ansible_host=<ip-address>
    caad-rob ansible_host=<ip-address> ansible_port=<port>
    caadlab-01 ansible_host=<fqdn>
    caad-10k ansible_host=<fqdn> ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q pwolfe@<fqdn>"'

    [caad:vars]
    ansible_user=pwolfe
    ansible_ssh_private_key_file=<key-location>

    [moc]
    moc-main ansible_host=<ip-address>
    moc-secondary-1 ansible_host=<ip-address> ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q pwolfe@<ip-address>"'
    moc-secondary-2 ansible_host=<ip-address> ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q pwolfe@<ip-address>"'

    [moc:vars]
    ansible_user=pwolfe
    ansible_ssh_private_key_file=<key-location>

    [cloudlab]

    [cloudlab:vars]
    ansible_user=pwolfe
    ansible_ssh_private_key_file=<key-location>
    ```
1. [Notes](https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-configure-a-jump-host-to-access-servers-that-i-have-no-direct-access-to) on how to use jump hosts to access servers that are not directly reachable. (e.g. secondary nodes on OpenStack)
1. Some caveats: It would appear that creating aliases for certain hosts requires you not use underscore '_' otherwise trying to specify such hostnames in commands results in such messages as:
    ```
    [WARNING]: Could not match supplied host pattern, ignoring: moc_openstack
    ```
1. Also, in order to be able to call hosts that need a password rather than providing an ssh file, it is necessary to install sshpass as follows: `sudo apt install sshpass` Then, when testing the ping command with a particular host one can call either `ansible moc-openstack -m ping` when an ssh key exists or `ansible caad-pf -k -m ping` when one does not exist and the user will instead be prompted to enter a password. When applied to a group, the command is evaluated on each in order but there seem to be some challenges when a group contains hosts that use an ssh key and those that take a password. (In general the preference/recommendation is to use an ssh key)
1. It is possible to configure the hosts to proxy through another node for access such as with the OpenStack VMs on the MOC that can be accessed via the main node. By defining a ProxyCommand (Note, the same ssh key is used for both and this appears to work fine, I have not found a working way to proxy through a node that takes a password into another node that takes a password such as caad-10k...)
1. I can see success with the MOC nodes by calling `ansible moc -m ping` and despite the different access methods defined they all respond the the ping successfully
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible moc -m ping
    moc-main | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python3"
        },
        "changed": false,
        "ping": "pong"
    }
    moc-secondary-2 | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python3"
        },
        "changed": false,
        "ping": "pong"
    }
    moc-secondary-1 | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python3"
        },
        "changed": false,
        "ping": "pong"
    }
    # The live command suggested for testing also works..
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible moc -a "/bin/echo hello"
    moc-main | CHANGED | rc=0 >>
    hello
    moc-secondary-2 | CHANGED | rc=0 >>
    hello
    moc-secondary-1 | CHANGED | rc=0 >>
    hello
    ```
1. General notes about ad-hoc commands: `ansible [pattern] -m [module] -a "[module options]"`
1. Making a test playbook, I am able to run it successfully. I have two observations after getting this working though, first when checking the validity of a playbook with ansible-lint, asking for "latest" version of a package vs "present" or a specific release results in an error (this is in order to try and encourage making repeatable runs). Additionally, when proxying through one host to another using an ssh key, it is much easier to preload the keys into ssh-agent and then call ansible, otherwise you cannot enter an ssh key password as needed because all of the hosts are being interacted with by the playbook. See below for examples of these comments.
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible-lint documentation/ansible_test.yaml 
    \WARNING  Listing 4 violation(s) that are fatal
    [403] Package installs should not use latest
    documentation/ansible_test.yaml:6
    Task/Handler: Upgrade all packages

    [403] Package installs should not use latest
    documentation/ansible_test.yaml:10
    Task/Handler: Install OpenMPI

    [403] Package installs should not use latest
    documentation/ansible_test.yaml:14
    Task/Handler: Install Libsodium

    [403] Package installs should not use latest
    documentation/ansible_test.yaml:18
    Task/Handler: Install OpenSSH server

    You can skip specific rules or tags by adding them to your configuration file:                                                                                      

    ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ # .ansible-lint                                                                                                                                                  │
    │ warn_list:  # or 'skip_list' to silence them completely                                                                                                          │
    │   - '403'  # Package installs should not use latest                                                                                                              │
    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible-lint documentation/ansible_test.yaml 
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible-playbook documentation/ansible_test.yaml

    PLAY [configure mpc environment] ***********************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************
    fatal: [moc-secondary-1]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh_exchange_identification: Connection closed by remote host", "unreachable": true}
    Enter passphrase for key '/home/pwolfe/.ssh/moc.key': fatal: [moc-secondary-2]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh_exchange_identification: Connection closed by remote host", "unreachable": true}

    [ERROR]: User interrupted execution
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ source add_moc_key_to_agent.sh 
    Agent pid 180
    Enter passphrase for /home/pwolfe/.ssh/moc.key: 
    Identity added: /home/pwolfe/.ssh/moc.key (/home/pwolfe/.ssh/moc.key)
    2048 SHA256:VrE4fbjx8BhhzA9nHtLiDv08dMkTNYckKsscWOaJziY /home/pwolfe/.ssh/moc.key (RSA)
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible-playbook documentation/ansible_test.yaml

    PLAY [configure mpc environment] ***********************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-2]
    ok: [moc-secondary-1]

    TASK [Install OpenMPI] *********************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]

    TASK [Install Libsodium] *******************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]

    TASK [Install OpenSSH server] **************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]

    PLAY RECAP *********************************************************************************************************************************************************
    moc-main                   : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-1            : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-2            : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    ```
1. There are some interesting challenges when using imported tasks and vars in ansible. Currently splitting them into separate files seems like a better appraoch. Organizing all of these vars and tasks files into a directory structure is probably for the best long-term.
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject$ ansible-playbook scripts/ansible/ansible_test.yaml -K
    BECOME password: 

    PLAY [Configure mpc environment by OS] *****************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Do OS specific setup needed before installing all packages] **************************************************************************************************
    included: /mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible/tasks_os_Ubuntu.yaml for moc-main, moc-secondary-1, moc-secondary-2, pf-test-vm

    TASK [Add scorep repository from PPA and install its signing key on Ubuntu target] *********************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Set OS distribution dependent variables] *********************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Install "{{ required_package }}] *****************************************************************************************************************************
    ok: [moc-main] => (item=make)
    ok: [moc-secondary-2] => (item=make)
    ok: [moc-secondary-1] => (item=make)
    ok: [moc-main] => (item=gcc)
    ok: [moc-secondary-2] => (item=gcc)
    ok: [moc-secondary-1] => (item=gcc)
    ok: [moc-main] => (item=openmpi-bin)
    ok: [moc-secondary-2] => (item=openmpi-bin)
    ok: [moc-secondary-1] => (item=openmpi-bin)
    ok: [moc-main] => (item=libsodium-dev)
    ok: [moc-secondary-2] => (item=libsodium-dev)
    ok: [moc-secondary-1] => (item=libsodium-dev)
    ok: [moc-main] => (item=openssh-server)
    ok: [moc-secondary-2] => (item=openssh-server)
    ok: [moc-main] => (item=scorep)
    ok: [moc-secondary-1] => (item=openssh-server)
    ok: [moc-secondary-2] => (item=scorep)
    ok: [moc-secondary-1] => (item=scorep)
    changed: [pf-test-vm] => (item=make)
    ok: [pf-test-vm] => (item=gcc)
    ok: [pf-test-vm] => (item=openmpi-bin)
    ok: [pf-test-vm] => (item=libsodium-dev)
    ok: [pf-test-vm] => (item=openssh-server)
    ok: [pf-test-vm] => (item=scorep)

    PLAY RECAP *********************************************************************************************************************************************************
    moc-main                   : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-1            : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-2            : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    pf-test-vm                 : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    ```
1. More debugging accomplished with rsync and properly setting file permissions
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible$ ansible-playbook ansible_test.yaml -K
    [WARNING]: Ansible is being run in a world writable directory (/mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible), ignoring it as an ansible.cfg source.
    For more information see https://docs.ansible.com/ansible/devel/reference_appendices/config.html#cfg-in-world-writable-dir
    BECOME password: 

    PLAY [Configure mpc environment by OS] *****************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-2]
    ok: [moc-secondary-1]
    ok: [pf-test-vm]

    TASK [Do OS specific setup needed before installing all packages] **************************************************************************************************
    included: /mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible/tasks_os_Ubuntu.yaml for moc-main, moc-secondary-1, moc-secondary-2, pf-test-vm

    TASK [Add scorep repository from PPA and install its signing key on Ubuntu target] *********************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Set OS distribution dependent variables] *********************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Install "{{ required_package }}] *****************************************************************************************************************************
    ok: [moc-main] => (item=make)
    ok: [moc-secondary-2] => (item=make)
    ok: [moc-secondary-1] => (item=make)
    ok: [pf-test-vm] => (item=make)
    ok: [moc-main] => (item=gcc)
    ok: [moc-secondary-2] => (item=gcc)
    ok: [moc-secondary-1] => (item=gcc)
    ok: [pf-test-vm] => (item=gcc)
    ok: [moc-main] => (item=openmpi-bin)
    ok: [moc-secondary-2] => (item=openmpi-bin)
    ok: [moc-secondary-1] => (item=openmpi-bin)
    ok: [pf-test-vm] => (item=openmpi-bin)
    ok: [moc-main] => (item=libsodium-dev)
    ok: [moc-secondary-2] => (item=libsodium-dev)
    ok: [moc-secondary-1] => (item=libsodium-dev)
    ok: [moc-main] => (item=openssh-server)
    ok: [pf-test-vm] => (item=libsodium-dev)
    ok: [moc-secondary-2] => (item=openssh-server)
    ok: [moc-main] => (item=scorep)
    ok: [moc-secondary-1] => (item=openssh-server)
    ok: [pf-test-vm] => (item=openssh-server)
    ok: [moc-secondary-2] => (item=scorep)
    ok: [moc-main] => (item=libz-dev)
    ok: [moc-secondary-1] => (item=scorep)
    ok: [pf-test-vm] => (item=scorep)
    ok: [moc-secondary-2] => (item=libz-dev)
    ok: [moc-secondary-1] => (item=libz-dev)
    ok: [pf-test-vm] => (item=libz-dev)

    TASK [Ensure mpc group exists] *************************************************************************************************************************************
    changed: [moc-main]
    ok: [pf-test-vm]
    changed: [moc-secondary-1]
    changed: [moc-secondary-2]

    TASK [Adding existing user "{{ item }}" to group mpc] **************************************************************************************************************
    ok: [pf-test-vm] => (item=pwolfe)
    changed: [moc-main] => (item=pwolfe)
    changed: [moc-secondary-2] => (item=pwolfe)
    changed: [moc-secondary-1] => (item=pwolfe)

    TASK [Create directories if they don't exist] **********************************************************************************************************************
    changed: [moc-main] => (item=/mpc/)
    changed: [moc-secondary-1] => (item=/mpc/)
    changed: [moc-secondary-2] => (item=/mpc/)
    changed: [pf-test-vm] => (item=/mpc/)

    TASK [Synchronize local files to remote hosts using rsync protocol (push)] *****************************************************************************************
    changed: [moc-main]
    changed: [moc-secondary-2]
    changed: [moc-secondary-1]
    changed: [pf-test-vm]

    PLAY RECAP *********************************************************************************************************************************************************
    moc-main                   : ok=9    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-1            : ok=9    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-2            : ok=9    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    pf-test-vm                 : ok=9    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    ```
1. Added automatic build, run, and output retrieval for exp-exchange. Note: I needed to use ansible.cfg to enable SSH Agent forwarding in order for mpi to run properlly. There are also some hard-coded values (such as ip addreses that I want to eliminate)
    ```
    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible$ ansible-playbook ansible_test.yaml -K
    BECOME password: 

    PLAY [Configure mpc environment by OS] *****************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Check Agent Forwarding - find loaded keys] *******************************************************************************************************************
    changed: [moc-main]
    changed: [moc-secondary-2]
    changed: [pf-test-vm]
    changed: [moc-secondary-1]

    TASK [Check Agent Forwarding - display loaded keys] ****************************************************************************************************************
    ok: [moc-main] => {
        "msg": "2048 SHA256:VrE4fbjx8BhhzA9nHtLiDv08dMkTNYckKsscWOaJziY /home/pwolfe/.ssh/moc.key (RSA)"
    }
    ok: [moc-secondary-1] => {
        "msg": "2048 SHA256:VrE4fbjx8BhhzA9nHtLiDv08dMkTNYckKsscWOaJziY /home/pwolfe/.ssh/moc.key (RSA)"
    }
    ok: [moc-secondary-2] => {
        "msg": "2048 SHA256:VrE4fbjx8BhhzA9nHtLiDv08dMkTNYckKsscWOaJziY /home/pwolfe/.ssh/moc.key (RSA)"
    }
    ok: [pf-test-vm] => {
        "msg": "2048 SHA256:VrE4fbjx8BhhzA9nHtLiDv08dMkTNYckKsscWOaJziY /home/pwolfe/.ssh/moc.key (RSA)"
    }

    TASK [Do OS specific setup needed before installing all packages] **************************************************************************************************
    included: /mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible/tasks_os_Ubuntu.yaml for moc-main, moc-secondary-1, moc-secondary-2, pf-test-vm

    TASK [Add scorep repository from PPA and install its signing key on Ubuntu target] *********************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Set OS distribution dependent variables] *********************************************************************************************************************
    ok: [moc-main]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]
    ok: [pf-test-vm]

    TASK [Install "{{ required_package }}] *****************************************************************************************************************************
    ok: [moc-main] => (item=make)
    ok: [moc-secondary-2] => (item=make)
    ok: [pf-test-vm] => (item=make)
    ok: [moc-secondary-1] => (item=make)
    ok: [moc-main] => (item=gcc)
    ok: [moc-secondary-2] => (item=gcc)
    ok: [moc-secondary-1] => (item=gcc)
    ok: [pf-test-vm] => (item=gcc)
    ok: [moc-main] => (item=openmpi-bin)
    ok: [moc-secondary-2] => (item=openmpi-bin)
    ok: [moc-secondary-1] => (item=openmpi-bin)
    ok: [pf-test-vm] => (item=openmpi-bin)
    ok: [moc-main] => (item=libsodium-dev)
    ok: [moc-secondary-2] => (item=libsodium-dev)
    ok: [moc-secondary-1] => (item=libsodium-dev)
    ok: [moc-main] => (item=openssh-server)
    ok: [pf-test-vm] => (item=libsodium-dev)
    ok: [moc-main] => (item=scorep)
    ok: [moc-secondary-2] => (item=openssh-server)
    ok: [moc-secondary-1] => (item=openssh-server)
    ok: [pf-test-vm] => (item=openssh-server)
    ok: [moc-main] => (item=libz-dev)
    ok: [moc-secondary-2] => (item=scorep)
    ok: [moc-secondary-1] => (item=scorep)
    ok: [pf-test-vm] => (item=scorep)
    ok: [moc-secondary-2] => (item=libz-dev)
    ok: [moc-secondary-1] => (item=libz-dev)
    ok: [pf-test-vm] => (item=libz-dev)

    TASK [Ensure mpc group exists] *************************************************************************************************************************************
    ok: [moc-main]
    ok: [pf-test-vm]
    ok: [moc-secondary-1]
    ok: [moc-secondary-2]

    TASK [Adding existing user "{{ item }}" to group mpc] **************************************************************************************************************
    ok: [moc-main] => (item=pwolfe)
    ok: [moc-secondary-2] => (item=pwolfe)
    ok: [pf-test-vm] => (item=pwolfe)
    ok: [moc-secondary-1] => (item=pwolfe)

    TASK [Create directories if they don't exist] **********************************************************************************************************************
    ok: [moc-main] => (item=/mpc/)
    ok: [moc-secondary-1] => (item=/mpc/)
    ok: [moc-secondary-2] => (item=/mpc/)
    ok: [pf-test-vm] => (item=/mpc/)

    TASK [Synchronize local files to remote hosts using rsync protocol (push)] *****************************************************************************************
    changed: [moc-main]
    changed: [moc-secondary-2]
    changed: [moc-secondary-1]
    changed: [pf-test-vm]

    TASK [Build the exp-exchange program (with parameters set in Makefile)] ********************************************************************************************
    changed: [moc-main]
    changed: [moc-secondary-1]
    changed: [pf-test-vm]
    changed: [moc-secondary-2]

    TASK [Attempting to launch experiment...] **************************************************************************************************************************
    skipping: [moc-secondary-1]
    skipping: [moc-secondary-2]
    skipping: [pf-test-vm]
    changed: [moc-main]

    TASK [Get files in a folder] ***************************************************************************************************************************************
    skipping: [moc-secondary-1]
    skipping: [moc-secondary-2]
    skipping: [pf-test-vm]
    ok: [moc-main]

    TASK [Find latest file] ********************************************************************************************************************************************
    ok: [moc-main]
    skipping: [moc-secondary-1]
    skipping: [moc-secondary-2]
    skipping: [pf-test-vm]

    TASK [Latest file name] ********************************************************************************************************************************************
    ok: [moc-main] => {
        "msg": ""
    }
    skipping: [moc-secondary-1]
    skipping: [moc-secondary-2]
    skipping: [pf-test-vm]

    TASK [Retrieving csv output] ***************************************************************************************************************************************
    skipping: [moc-secondary-1]
    skipping: [moc-secondary-2]
    skipping: [pf-test-vm]
    changed: [moc-main]

    PLAY RECAP *********************************************************************************************************************************************************
    moc-main                   : ok=17   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    moc-secondary-1            : ok=12   changed=3    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0   
    moc-secondary-2            : ok=12   changed=3    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0   
    pf-test-vm                 : ok=12   changed=3    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0   

    pwolfe@Lux:/mnt/d/Documents/BU Cloud/repos/ccproject/scripts/ansible$ cat ../../retrieved/201129_181225_exp-exchange_log.csv 
    ROWS,GENSHR,SEEDS,BATCHED,SYNC,ASYNC,
    100,0.030386886,0.000282848,0.000052135,0.006204539,0.005937755,
    100,0.000265697,0.000132516,0.000034384,0.005812358,0.005817240,
    100,0.000263630,0.000165586,0.000019571,0.006538443,0.005517263,
    1000,0.002190089,0.000254893,0.000023473,0.054127668,0.048974975,
    1000,0.002153668,0.000271364,0.000021111,0.046066088,0.047589445,
    1000,0.002116655,0.000269891,0.000019217,0.059231410,0.062936868,
    10000,0.022966118,0.000944601,0.000666915,0.515776584,0.501193793,
    10000,0.022857463,0.000862909,0.000877864,0.545248115,0.547991850,
    10000,0.023044037,0.000807869,0.000874716,0.514174577,0.495143399,
    100000,0.238377837,0.005558039,0.008037779,5.427168364,5.399003084,
    100000,0.228624684,0.007648385,0.008436066,5.902135834,6.098306454,
    100000,0.227035462,0.007446744,0.007952234,5.954678891,5.648029217,
    ```

## Notes:
1. Make sure to recall basic constructs and syntax when using [YAML](https://en.wikipedia.org/wiki/YAML) [A readable introduction](https://camel.readthedocs.io/en/latest/yamlref.html)
1. Make a call to ansible using the `-k` or '-K' flags for login password or escalation password when connecting to a host as a non-root user.
1. In order to make everything work on CloudLab I needed to add my nodes to the hosts file, I also needed to change the playbook to specify the correct hostname for the master node (I should change this to ansible roles). Finally, I created mpc.conf which I can copy over the the master node and place in `/etc/ssh/ssh_config.d/` in order to avoid strictly checking the ssh key (which otherwise makes the automatic mpi call hang)
