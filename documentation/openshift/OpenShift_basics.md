# An Introduction to Redhat OpenShift
## *Author: Hasnain Abdur Rehman*
### Purpose: To Learn Application deployment on Redhat OpenShift and Deploy MPC Code 
### *These are notes I made when taking the Udemy course "OpenShift for Absolute Beginners" for the CC project-- this can be used by team members/mentors/future users to understand how containers work.* 
&nbsp;
&nbsp;

## OpenShift is RedHat's **Open source Container Application Platform** for developing and hosting enterprise level applications. 
&nbsp;
&nbsp;

OpenShift OKD (formerly OpenShift Origin) is based on top of **Docker containers** and **Kubernetes Cluster manager**, with added developerment and operational centric tools that enable rapid application development, deployment and lifecycle management.

-   Docker: Creates ***images*** of ***application with prepackaged dependencies*** into deployable images.
-   Kubernetes: Powers deployment and management of Docker images across large clusters by providing self-healing and auto-scaling features.

Open Shift builds on these Docker/Kubernetes by providing layer of tools that abstracts Kubernetes and infrastructure management tasks to help developers easily deploy applications.
&nbsp;

*A side-note about Docker: Docker containers share the underlying kernel. Windows does not share kernel with linux OS's, so Docker won't run a windows based container.*&nbsp;
&nbsp;

---
## Comparison of Containers vs VMs:
Each VM has its own OS running, then dependencies of an application then the application itself.&nbsp;


### Therefore, <ins>Hardware infrastructure is wasted as useless work for each OS, plus disk wastage for each VM. </ins> &nbsp;

In comparison, <ins>*Docker containers are lighter -- usually in MB's*. They ***boot up faster -- in seconds***.</ins> &nbsp;

**VM's boot slower -- in minutes, since the whole OS boots.** 
Docker has less deployment isolation as more resources are shared -- however, VMs are completely distinct from each other. &nbsp;

---
## Containerized versions of applications are available on Dockerhub.
We can find images of DB's, OS's, etc. can be found. As example, simply typing Docker run **application_name* runs a container: &nbsp;

Docker run ansible &nbsp;

Docker run mongodb&nbsp;

Docker run nodejs

--- 

## Understanding Docker images: 
A Docker Image is a template. Containers are instantiated from images. 
Images also help in shipping a working, or already setup version of application, therefore streamlining deployment. 

---

## Kubernetes:
Container orchestration technology that orchestrates deployment and management of hundreds of containers in a clustered environment. 
Demand increases -> deploy more instances. 
Object configuration files are used.

---
## MiniShift:

Mini-Shift: A local instance of Open Shift Cluster that can run on Windows.

---
## Some OpenShift CLI commands: 

oc login http://mycluster.company.com
oc login
oc login -u developer -p developer
oc logout

---
## OpenShift Projects 

A large Kubernetes cluster can host hundreds of pods and many deployments.   &nbsp;

Project: allows organize and manage content.  &nbsp;

Isolates work.  &nbsp;

Manage access to resources.  &nbsp;

Projects are built on top of Namespaces. &nbsp;

Objects are prefixed with your selected namespace -> grouping functionality for resources. &nbsp;

Openshift takes care of namespaces itself by using project names. &nbsp;

&nbsp;

When we add an application to project, Openshift  automatically creates a build job for the application using the URL for the SCM repository. 
&nbsp;

'Build' downloads a copy of code from the repo and builds the code using a predefined build configuration into a docker image. &nbsp;

The docker image is then pushed to the built in Docker registry.&nbsp;

Openshift also creates a deployment automatically. &nbsp;

After a successful build the deployment deploys the application using the image from the internal Docker registry to the Kubernetes Cluster, making application available to the end users. &nbsp;


---



## Build Strategy

1.  Docker Build: Make a *Docker-File* and provide instructions, e.g. FROM ubuntu:16.04 RUN apt-get update ,etc. 
2.   s2i: OpenShift 'Source to Image' Tool. No need for a Docker-File. Uses a pre-built builder image and injects application code into it to create the final application image. When we do the normal catalogue Python addition, a build configuration of s2i is made. 

### To modify build configuration, use a YAML file or edit build config from web console. 

---
## Image Streams: 

Map Docker images hosted at different locations to image names within projects. All dependent images get a consistent reference. Image stream is abstracted by an image ID which is unique across builds. If an build configuration that makes of use of Python updates its python, our already deployed applplication which was instantiated from an image containing older python won't be affected, since it is using an image ID, and image ID would refer to the consistent Python installation.

---

## Creating a New Build Configuration: &nbsp;

Edit or make your own YAML file then upload it to OpenShift. 

---

## Build Triggers: LAUNCHING CI/CD
Manual making builds is not continuous integration.  &nbsp;

We need an automatic detection of source code change and then automatic building and deployment in target environment. &nbsp;

This is done using Web-hooks.  &nbsp;

---
## Web-hooks: 

Web-hooks are an event notification technique that sends HTTP POST req. to a URL when a code change occurs. GITHUB has built in facility. Add openshift URL there. URL can be found in OPENSHIFT. 

---
## Deployments:

### Pods: Smallest deployment in Kubernetes. &nbsp;

Essentially one or more Docker Containers that are dependent on each other - grouped together.  &nbsp;

Usually its just a single container in a pod. &nbsp;

Think of pod as a single instance of Docker container running our application.  &nbsp;

For scalability and high availability, we need multiple instances of our application running.  We need replication of our pods. This is done through replication controllers.  &nbsp;

Replication controllers ensure required number of replicas of our application are running at all times.  &nbsp;

Next in hierarchy is Deployment.  &nbsp;

A deployment builds on rep controllers with additional support for application lifecycle management such as seamless upgrades, roll backs , application revisioning, etc.  &nbsp;

When an application is added to the project, a build configuration as well as a deployment is made.  &nbsp;sss

--- 

## Deployment Strategies:
1.  Rolling Strategy: If we had multiple replicas, updating application would cause the deployment to update replicas one at a time. 

2.  Recreate Strategy: Destroy all, then create new ones all at one time with the new build configuration. 

#### -> Default is rolling update.  &nbsp;

Blue/Green Strategy: Blue is older version, Green is newer.  &nbsp;

We run both together. If Green is okay, we switch users to Green.  &nbsp;

A/B Strategy: Small percentage to users to new one. Gradually increase this percentage. 


---

## Networking in OpenShift: &nbsp;

Kubernetes cluster is composed of master and worker nodes. &nbsp;

Each of these are virtual/physical machines, they all have their own IPs. &nbsp;

Each pod gets an IP address of its own. A fundamental requirement  is communication between pods. They must be on a network and have unique IP addresses.  &nbsp;

Openshift Software-defined network -> creates a virtual (overlay) network, made using Open vSwtich standard.  &nbsp;

Open vSwitch is a distributed virtual switch used to interconnect VMs in a hypervisor. &nbsp;

Default network ID for overlay network is 10.128.0.0/14. &nbsp;

Each note is assigned a unique subnet.  &nbsp;

10.128.2.0 &nbsp;

10.128.4.0 &nbsp;

Do oc get pods -o wide gives IP addresses of each pod. &nbsp;

Restarting a pod changes IP. Therefore DNS is used.  &nbsp;

---

## Services:

Connect pods/applications independently of IP or DNS. &nbsp;

Its better to use service for connectivity since service acts as a load balancer for each section of our microservices architecture.  &nbsp;

Each service has it is own  IP and DNS. &nbsp;

Its called Cluster IP because its kind of an internal IP address, for internal communication.  &nbsp;

Selectors link pods to services. And use Service port, plus target port. &nbsp;

---

## Routes: 

Helps us expose service to external users through a host name.  &nbsp;

Balances load on different pods. 


 






































