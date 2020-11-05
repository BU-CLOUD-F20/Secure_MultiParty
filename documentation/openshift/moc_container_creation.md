# OpenShift Instructions

## Following OpenShift Introduction
*Based on [these](https://learn.openshift.com/introduction) instructions*

1. Download and install the OpenShift CLI tool "oc"
    1. On Ubuntu (WSL1 - Ubuntu 18.04.5 LTS) I searched using `apt search OpenShift` and then obtained one result which I inspected using `apt show rhc/bionic`
    1. The MOC documentation points to the OpenShift [github repository](https://github.com/openshift/origin/releases) for obtaining the oc CLI tool. Specifically it mentions downloading the [v1.5.1](https://github.com/openshift/origin/releases/v1.5.1/) openshift-origin-client-tools but this was released in 2017 so I suspect we may want a newer version instead... After checking to find the [most recent release available](https://github.com/openshift/origin/releases/latest) I followed the following modified steps from the MOC guide:
        ```
        # I downloaded the most recent package:
        wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
        # Unpacked
        tar -xzvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
        # Moved/renamed
        mv openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit oc-tool
        # Changing directory into oc-tool I can now run the commands
        # I could add the following to my .bashrc to avoid adding the directory to my
        # PATH manually at each launch. i.e.
        # export PATH=<HOME>/oc-tool:$PATH
        ```

    1. Following that, to login I have the following choices:
        ```
        oc login
        # Then enter the openshift cluster url when prompted
        # e.g. https://k-openshift.osh.massopen.cloud:8443
        # Or to use an existing token from the web portal, copy the following with the
        # unhidden token
        oc login https://k-openshift.osh.massopen.cloud:8443 --token=<hidden>
        ```

        ![openshift1](/Images/openshift1.png)

1. *To be continued when OpenShift is restored... currently experiencing some difficulties on the MOC*

*The MOC OpenShift Documentation is [here](https://docs.massopen.cloud/en/latest/openshift/OpenShift.html)*
