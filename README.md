# Secure_MultiParty Background Information:
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

---
# Project Proposal:

## Team Members:
Role | Name | Email
-----|------|------
Developer | Hasnain Abdur Rehman| hasnain@bu.edu
Developer | Pierre-François Wolfe | pwolfe@bu.edu
Developer | Samyak Jain | samyakj@bu.edu
Developer | Suli Hu | sulihu@bu.edu
Developer | Yufeng Lin | yflin@bu.edu
Mentor/Client | John Liagouris | liagos@bu.edu
Mentor/Client | Vasiliki Kalavri | vkalavri@bu.edu
Subject-Matter Expert | Mayank Varia | varia@bu.edu

## Team Typical Schedule:
*Note: Times in EST*
![team_schedule_placeholder](Images/team_schedule_placeholder.png)

# 1. Visions and Goals of the Project:

## Vision Statement
This project aims to deploy a C-based implementation of a 3-party Secure Multi Party Computation program on the Mass Open Cloud under multiple cloud-based and simple bare-metal deployment configurations. After deployment, the project will perform performance analysis on the different deployments using some standardized benchmarks, and compare the performance of Secure-MPC on the different deployments. Finally, the project will try to optimize the cloud based optimizations and search for possible bottlenecks, tweaks and try to leverage cloud-environment to improve performance of the MPC on cloud.

## Goals
A simplified breakdown of the project into high level goals includes:

* Deployment of the Secure-MPC on multiple cloud-based and bare-metal platforms.
* Functionality testing and verification of deployments.
* Profiling and comparing each deployment configuration on [Massachusetts Open Cloud (MOC)](https://massopen.cloud/) with respect to some benchmark specifications.
* Design space exploration of the Secure MPC deployments to increase performance/benchmark scores.
* Determining the best performing deployment configuration across all deployments done.

**__Questions:__**
* Configuration/launch tools to recreate different run scenarios on the MOC?
  * Automated testing/profiling chain to gather new data with different changes?
  * Improved frontend? What is the current user interface and who can/can't make use of it?
    * Are we appropriately serving the target user audience? (Domain experts, outsiders, other?)
  * Improved backend?


---
# 2. Users/Personas of the Project:

## Users/Personas of Interest
Since this is a deployment of a specialized MPC implementation as a research-output on the Mass Open Cloud, the quintessential users of this project would be the initial MPC development team.

## Users/Personas List
* John
* Vasia
* John and Vasia's Research Team
* Further users may include
  * MOC Client using MPC
    * MPC non-expert sub-type
    * Cloud Computing non-expert sub-type
  * Researchers using MPC on MOC
    * Current project clients
    * Future researchers
    * Students
    * Cloud Administrator
    * Providers/Individuals acting as separate MPC parties/evaluators?

---
# 3. Scope and Features of the Project:

The project scope includes:

* Deployment of the Secure MPC on the following platforms:
  * Virtual Machines (using OpenStack)
  * Containers (using OpenShift)
  * Bare Metal Machines (using OpenStack)
* Generation of repeatable execution configurations and a generalized interface for the cloud deployments.
  * Creating launching scripts and editing configuration files.
  * Providing greater ease of use/recreation of specific modes/tests.
* Functionality testing and verification of the deployments.
* Profiling and comparing the deployment configurations on [Massachusetts Open Cloud (MOC)](https://massopen.cloud/)
  * Determining appropriate performance representative benchmark specifications and metrics for the MPC deployments
  * Writing/Coding benchmark tests for each deployment.
  * Measuring the benchmark scores.
  * Generating a comparison report.

STRECH Features  >>>>> ???????
* Design space exploration of the Secure MPC deployments to increase performance/benchmark scores.
  * Configuring MPI settings and trying different modes (sync vs async) to achieve minimal communication bottleneck.
  * Testing communication protocols other than MPI to gain performance improvement.
  * Exploring alternatives to the current single-process per party paradigm.
  * Identifying bottlenecks and other areas for improvement to the library as implemented.
  * Multiple pthreads ...????
  * OpenMP ....????
* Determining the best performing deployment configuration across all deployments made.

The following are clearly being mentioned to be out of scope of this project:   
* A GUI for the Secure-MPC deployments (for outside clients who might want to use a generalized or configured version of the software).

---
# 4. Solution Concept:

## High-level Solution Outline

## Architectural Diagrams
![simple_mpc_arch](Images/simple_mpc_arch.png)

*TODO - Diagram Ideas*
* Illustrate MPC system possible implementations on MOC
  * Software/Hardware Stack
  * User perspective of launching an MPC evaluation
  * Identify some primary interfaces/aspects that will be profiled
  * Add a walkthrough explanation for all included diagrams and the system as a whole
  * Idea: make sure to color elements that are within project scope to make them visually identifiable!
* Make sure to identify all dependencies!
  * Currently the only dependency is on [libsodium](https://doc.libsodium.org/)
  * Otherwise the software only uses standard C

## Design Implications and Discussion
*TODO - Will evolve as project scope is more clearly defined and work takes place*
* Identify which parts of the system are of concern and which are part of another party's scope (e.g. things that are already handled by the MOC)

**__Questions:__**
* Will need to see existing code to create a better sketch of the current architecture.
* Will need to find out more about the MOC to identify possible architecture/deployments
* Once user stories/vision is known we can define if there are specific frontend or backend architectures to define.

---
# 5. Acceptance Criteria:
* Provision of a thorough survey report of the software over a comprehensive set of deployment configurations with the range of software settings tested.
  * Make it possible to recreate the tested implementations.
  * Identification bottlenecks in tested implementations.
  * Selection of execution scenarios with the greatest potential.

**__Questions:__**
* Will this be purely or mostly performance based? What are the metrics?
* What features or outcome is sought?
* Can be define minimal goals (MVP) as well as stretch goals?
* If this is to be conducted primarily as a survey, what is the desired minimum reasonable amount of testing to be accomplished?

---
# 6. Release Planning:
*TODO: This section will need to show how incremental features and functions will be delivered...*
- [ ] Identify user stories
- [ ] Associate user stories with different releases (One "release" per sprint with 5 sprints for the project)
  * This should ease/guide sprint/planning sessions
  * The initial iteration is expected/likely to have higher-level details.
  * Detailed user stories and plans to be detailed on [taiga](https://tree.taiga.io/project/jonathanchamberlain-performance-analysis-of-secure-multi-party-computations-in-the-cloud/timeline)

## Some Preliminary Goals by Sprint:
  * Pre-Sprint:
    - [X] Establish Team Communication (Slack/Zoom)
    - [X] Initial Mentor meeting
    - [ ] Finalize Ongoing Meeting date (Proposed: Mondays EST 3-4PM)
      - [ ] Additional occasional evening meeting for different time zones? Or alter proposed meeting regular meeting time?
    - [ ] Establish Project Plan (due by September 17, 2020)
    - [ ] Gain access to existing software ASAP
    - [ ] MPC, MPI, and other background reading as needed by team members (additional learning "spikes" expected in Sprint 1)
  * Sprint 1: September 17, 2020 - October 1, 2020
    - [ ] Work on task breakdown using taiga board
    - [ ] Schedule meeting with Mayank for MPC background presentation?
    - [ ] Gain MOC access and perform any necessary [background reading](https://docs.massopen.cloud/en/latest/home.html#) (Specifically look at the "How-Tos")
    - [ ] *TODO*
  * Sprint 2: October 1, 2020 - October 15, 2020
    - [ ] *TODO*
  * Sprint 3: October 15, 2020 - October 29, 2020
    - [ ] *TODO*
  * Sprint 4: October 29, 2020 - November 12, 2020
    - [ ] *TODO*
  * Sprint 5: November 12, 2020 - December 3, 2020
    - [ ] *TODO*

**__Questions:__**
* After answering earlier questions this will be easier to plan
* If this is mostly a survey, the sprints will likely consist of increasingly granular benchmarking.
* If there are certain performance metrics to reach or features to implement then initially profiling might be the main goal with later sprints using initial profiling as a baseline
  * Note: perhaps an initial sprint will be to create a more automated benchmarking setup to help assess progress in later sprints?

---
# General Comments:
*TODO*
* WIP Notes:
  * [Project Description Template](https://github.com/BU-NU-CLOUD-SP18/sample-project/blob/master/README.md)
  * [Example Project Description](https://github.com/BU-NU-CLOUD-SP18/sample-project/blob/master/MOC-UI-ProjectProposalExample.md)
  * [GitHub Markdown Reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
    * [Another Reference](https://docs.github.com/en/github/managing-your-work-on-github/about-task-lists)
