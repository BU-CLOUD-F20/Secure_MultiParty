# Secure_MultiParty
Performance analysis of secure multi-party computations in the cloud

Project Logistics:
Mentors: John Liagouris email: liagos@bu.edu;  Vasiliki Kalavri email: vkalavri@bu.edu; 
Will the project be open source: yes
 
Preferred Past Experience:
Strong C/C++ programming skills: Required
OpenStack/OpenShift: Nice to have
MPI (Message Passing Interface): Nice to have
MPC (Multi-Party Computation): Nice to have 

Project Overview:
Background: Secure multi-party computation (MPC) refers to a family of cryptographic protocols that allows distrustful parties to jointly perform arbitrary data computations while keeping the inputs and intermediate data of the computation private. Compared to traditional non-secure computations, MPC requires exchanging more data between parties and its performance relies heavily on the communication layer.
 
Project Specifics: In this project students will instrument and profile distributed MPC applications in the cloud with the goal to identify performance bottlenecks and potential optimizations. The analysis will focus on the networking layer. Students will experiment with different deployments, network libraries, and communication patterns (sync vs async) to identify optimal solutions based on the workload characteristics.

Some Technologies you will learn/use:
How to deploy applications in the cloud using VMs and OpenShift containers
How to instrument and profile distributed applications
MPI libraries: https://github.com/open-mpi/ompi , https://github.com/pmodels/mpich 
MPC protocols: https://www.youtube.com/watch?v=P2MmO458xu4 
