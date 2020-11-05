# Installing Libsodium on your VM

1. Following the suggestion from INSTRUCTIONS.md we will install Libsodium from the following [link](https://libsodium.gitbook.io/doc/installation) online.

    ![libsodium1](/Images/libsodium_image1.png)

1. It is recommended to use the distribution [tarballs of Libsodium](https://download.libsodium.org/libsodium/releases/) rather than the [github repository](https://github.com/jedisct1/libsodium) because the tarballs do not require any dependencies.

    ![libsodium2](/Images/libsodium_image2.png)

1. Download the latest `stable` tarball of libsodium from the above link and unzip it.

1. Copy the unzipped folder over to the VM using: `scp -i ~/.ssh/cloud.key -r libsodium-stable/ ubuntu@128.31.25.117:/home/ubuntu/ccproject`

    ![libsodium3](/Images/libsodium_image3.png)

    ![libsodium4](/Images/libsodium_image4.png)

1. After that, do the following to install Libsodium on the VM:

  `cd libsodium-stable`

  `./configure`

  `make && make check`

  `sudo make install`

1. Libsodium is successfully installed on the VM.

1. To use libsodium in a project, the header `sodium.h` should be included and the `sodium_init()` function should be called before any other function.

1. For more information on using libsodium refer to:  [quickstart](https://libsodium.gitbook.io/doc/quickstart) and [usage](https://libsodium.gitbook.io/doc/usage).



...now the next step may be to test the MPC codebase on a single node or to generate additional VMs.

To move the MPC codebase onto the VM: `scp -i ~/.ssh/cloud.key -r mpc_codebase/ ubuntu@128.31.25.117:/home/ubuntu/ccproject`


*TBD*
