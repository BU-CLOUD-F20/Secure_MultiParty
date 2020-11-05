# Open Cloud Testbed - CloudLab

## Initial CloudLab Setup
*Following the [Youtube video series](https://www.youtube.com/playlist?list=PL9rbrM_7FJbm6EgOswWuqcBoaS9m6s_JQ)*

1. After creating an account and new project or joining an existing project login to the CloudLab web interface.
1. Under Experiments click on "Start a New Experiment"
    1. Clicking "Change Profile" makes it possible to search for and select a different profile for this experiment.
    1. Specifically following the tutorial video, I am selecting the OpenStack profile with Repo Hash: 749e3586 then selecting "Next"
1. On the Parameterize page it is possible to change various settings. For the OpenStack profile the release can be chosen as well as the number of compute nodes, hardware type, link speed, and more.
    1. Note: The resource Availability pop-out window can be helpful when trying to pick specific hardware for the experiment.
    1. Advanced options hides many more settings that can be configured. I've left them as default for now following the video guide.
1. On the Finalize page I specify a name "tutorial-test" and select a cluster, trying to pick one that has resources available.
    1. For the test, I used the Utah cluster as suggested in the tutorial.
    1. Note: Federated clusters operate differently in that they are owned an operated by a set of different parties rather than being operated and owned by the same party. They all follow the same policy however so they operate in the same fashion.
1. On the schedule page I can just leave everything blank to start immediately. Then I just need to wait for the setup to be completed. Make sure to wait to get an email and then check that any nodes indicate "Finished" in the web interface.

    ![clab](/Images/clab.png)

    ![clab0](/Images/clab0.png)

1. Profile instructions can be expanded on this page and describe how to use CloudLab.
    1. There is a link to the OpenStack web interface for the experiment as well as a link to the Grafana interface. Additionally there is a link to the profile setup scripts. All three of these use the same username and automatically generated password.

        ![clab1](/Images/clab1.png)

        *OpenStack Dashboard Login*

        ![clab2](/Images/clab2.png)

        *OpenStack Dashboard*

        ![clab3](/Images/clab3.png)

        *Grafana Dashboard*

        ![clab4](/Images/clab4.png)

        *Profile Setup Scripts*

    1. On the List View tab in the web interface are each of the nodes as well as ssh access instructions.
        ```
        # First, make sure to follow the ssh instructions as noted in ssh_notes.md
        # Add the key generated for CloudLab to the ssh-agent before trying to access the nodes
        # When I ran my test case I had the following:
        ssh -p 22 pwolfe@ms1307.utah.cloudlab.us
        ssh -p 22 pwolfe@ms1326.utah.cloudlab.us
        ```
1. In the OpenStack Dashboard interface: Once logged in, if we want we can create a VM instance on our compute node using the "Launch Instance" button. The steps from here are essentially the same as those used on the MOC OpenStack instance (reference mov_vm_creation.md, cc-mpc-main_setup.md, and cc-mpc-secondary_setup.md for how to create and configure VMs in OpenStack). Pictures shown below for reference.

    ![clab5](/Images/clab5.png)

    ![clab6](/Images/clab6.png)

    ![clab7](/Images/clab7.png)

    ![clab8](/Images/clab8.png)

    ![clab9](/Images/clab9.png)

    ![clab10](/Images/clab10.png)

    ![clab11](/Images/clab11.png)

    *VM created on OpenStack experiment on baremetal in CloudLab*
