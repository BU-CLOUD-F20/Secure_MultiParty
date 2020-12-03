## Multi-bare-metal Nodes Setup

1. For multi-bare-metal setup, we originally use the five-bare-metal nodes profile provided by cloudlab.
  

2. For the experiment setup, simply follow the single bare metal node in the previous readme. While creating the experiment the Cloudlab Utah Cluster occationally failes because of the crowd, when this happens other clusters like Cloudlab Wisconsin can work well too.
  

3. After the experiment created, there is a listview of different bare metal nodes.

![clab](/Images/multinodes/1.png)
  
4. In order to communicate between different nodes, we use agent forwarding to pass over the key so we do not need to create new keys to connect new nodes. Firstly, we pass our private key to first node which is node-0, and then we can pass the key by ssh -A username@hostname.com 
  
![clab](/Images/multinodes/2.png) 

5. After setting up the forwarding agent, we can 'jump' from one node to the other nodes.

![clab](/Images/multinodes/3.png)

6. ```
   sudo apt update
   ``` 
   is required for setting up the environment. And then we do the same job on other nodes to test MPI functionality.

![clab](/Images/multinodes/4.png)

7. Next step is mark down the ip address by ifconfig command.


8. And now we can test the MPI functionality with ip address and other parameters specified using mpirun.
  
![clab](/Images/multinodes/5.png)

9. Now we are going to test the exp-exchange in the code base, since these multi bare metal nodes require c99, a past verison of the C programming language standard, we should specify it in the Makefile or the command would fail.
  
![clab](/Images/multinodes/7.png)
  
10. Since evry node is invloved in the multi baremetal system, remeber use `scp (secure copy)` to copy the executable binary file from local system to remote systems and make sure they have been install the depencencies (libsodium). Also, we need to create the same directory structure in order to see the results. In this case, we `scp` the executable from node-0 to node-1 and node-2.


![clab](/Images/multinodes/8.png)

11. Exp-exchange results 

![clab](/Images/multinodes/9.png)
  


