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
Developer | Hasnain Abdur | hasnain@bu.edu
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
The Cloud Computing MPC team will perform benchmarking of the MPC implementation provided by the projects mentors/sponsors John Liagouris and Vasiliki Kalavri in order to provide insights on existing bottlenecks. From there, these bottlenecks will be examined to provide actionable performance improvements.

## Goals
Accomplishing this will include:
* Profiling the existing software on the [Massachusetts Open Cloud (MOC)](https://massopen.cloud/) under different deployment configurations.
  * VMs (OpenStack)
    * Different OS's? Different kernels under the same OS?
  * Containers (OpenShift)
  * Bare Metal (OpenStack)
* Testing different communication configurations between computation parties
  * Changing the settings for MPI
  * Alternatives to MPI for communicating between processing parties?
* Exploring alternatives to the current single-process per party paradigm
  * Multiple pthreads
  * OpenMP
* Provide recreatable execution configurations and tests
  * Create launching scripts or similar
* Stretch goals
  * Enable running MPC implementation on top of a BU developed Linux micro-kernel
  * Evaluate performance of MPC with the micro-kernel

**__Questions:__**
* Is the final desired state meant to be "functionally the same" but with greater performance?
  * If so, is there some performance metric either relative or absolute that we should target?
    * Would that metric be based on some specific need (being able to do x many operations in y time)?
      * If so, add to acceptance criteria section
    * Canonical/reference tests to be used? Alternately, do these need to be developed or improved?
  * If not, what additional functionality or utility must be provided? (Some examples/ideas follow)
    * Configuration/launch tools to recreate different run scenarios on the MOC?
    * Automated testing/profiling chain to gather new data with different changes?
    * Improved frontend?
      * What is the current user interface and who can/can't make use of it?
      * Are we appropriately serving the target user audience? (Domain experts, outsiders, other?)
    * Improved backend?
      * Different MPC evaluation?
        * Change MPC primitives?
        * Make modifications to derived MPC operators?
        * Additional operators (extending functionality)?

---
# 2. Users/Personas of the Project:

## Users/Personas of Interest
The end-goal of this software is to be powerful and flexible enough to be attractive to non-MPC experts and provide a simple interface with greater performance than existing approachable software MPC alternatives. For the scope of this semester project however, we do not target a completely naïve user. Instead we require that a user be somewhat familiar with the concept of MPC. The goals are primarily performance oriented and are perhaps most appreciated by a more experienced user rather than a newcomer with no familiarity with the MPC offerings landscape.

## Users/Personas List
* MOC Client using MPC
  * MPC non-expert sub-type
  * Cloud Computing non-expert sub-type
* Researcher using MPC on MOC
  * Current project clients
  * Future researchers
  * Students
* Other personas that may become relevant?
  * Cloud Administrator?
  * Providers/Individuals acting as separate MPC parties/evaluators?

**__Questions:__**
* The above statement is conjecture, please confirm it...
  * Are we targeting a specific lowest denominator of user?
    * Non-MPC expert?
    * Non-Hardware expert?
    * Casual user? (Not familiar with software development)
  * It would seem reasonable to separate long-term desired users and users targeted for the scope of this project.
    * If we are unsure, it would seem wisest to divide into users certain to be targeted, possible targeted, and definitely not targeted.

---
# 3. Scope and Features of the Project:
MPC Profiling
* Provide researcher insights into existing codebase
  * Provide a "best" execution configuration for the existing codebase
  * Identify bottlenecks and other areas for improvement to the library as implemented.
* Provide greater ease of use/recreation of specific modes/tests
  * Launching scripts/configuration files
  * A GUI could be nice but is almost certainly out of scope as outside clients of the MPC are not the primary personas for this project.

**__Questions:__**
* This will need far more detail, answering the earlier questions will help to inform this section.
* Once we know what users and what the user stories/envisioned high-level outcome is we can better ask questions concerning scope specifics...

---
# 4. Solution Concept:
*TODO - Add to this!*

## High-level Solution Outline
* Use a diagram to illustrate a high-level concept of the solution
  * Alternately, the appearance of the solution can be shown here if there is already an architectural diagram that exists for the project.
  * Note: Consider using LucidChart since it is available to BU students.
  * A walkthrough of the diagramed structure should exist.

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
* Establish a performance baseline.
  * Compare to prior-testing/published results
* Provide a thorough survey of the same software over a comprehensive set of deployment configurations with a range of software settings.
  * Make it possible to recreate the tested implementations.
  * Identify bottlenecks in tested implementations.
    * Select execution scenarios with the greatest potential.

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
