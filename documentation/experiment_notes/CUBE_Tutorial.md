# CUBE for Data Analysis

Before reading this, you should have managed to run the mpi experiments, and have already collected some results.

This doc is helping you to better understand the data and gain some insights form it by using a data analysis tool called CUBE.

## What is CUBE ?

![image](https://github.com/jliagouris/ccproject/blob/master/Images/cube1.png)

CUBE is a presentation component suitable for displaying performance data for parallel programs including MPI and OpenOpenMP applications. The tool allows the interactive exploration of this space in a scalable fashion and browsing the different kinds of performance behavior with ease. CUBE also includes a library to read and write performance data as well as operators to compare, integrate, and summarize data from different experiments.

## How to get CUBE ?
1. Go to the website: https://www.scalasca.org/software/cube-4.x/download.html
2. In `Supplementary packages for download (Comfort zone)` Section chose your prefered version (We used mac for demonstration)
![image](https://github.com/jliagouris/ccproject/blob/master/Images/cube2.jpg)
3. After you downloaded this package, follow the insturctions and choose `default` when needed. (If you are using mac, you will see the logo in Applications Dir)

## How to use CUBE ?

### 0. Preparation before start:
1. An installed CUBE
2. The datas you want to deal with.

    In our experiments, the data was generated and collected by score-p running mpi in the openstack nodes.
    These look like:
    <img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube3.jpg width="450" alt="cube3"/>
3. Alternatively, if we do not have gui environment in our system, we can view textual output with the following command:

```
scorep-score -r profile.cubex
```


![cube](/Images/scorep-score.png)


And we can see there is a list including some information about the region visited, visited times and running time for each region etc.
    

### 1. Launch the CUBE
Launch the CUBE, and chose your data cubex file trhough `Open Cube File` button.
<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube4.png width="450" alt="cube4"/>
### 2. Home Page (3 Columns)

Here is one of the gui windows we examined. And there are 3 tags created manually explaining each column.
![cube](/Images/cubeguiexp.png)


In detail, the homepage generaly consists of 3 columns, looks like:
<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube5.jpg width="650" alt="cube5"/>

In the left columns, you can see the high-level datas you have, for instance, `Visits`, `Time` or `Dada Bytes`

In the mid columns, you can unfold the data you interested, for instance, if you want to see the detail time cost of Initialization, you can unfold the `5.14 exp exchange`-`5.14 main`-`1.01 init`, then you will know it consists of 3 parts, the MPI initialization, MPI comm rank and MPI comm size.

In the right columns, by clicking the Statistics in Tag Bar, you can see the graphical statistic info of your current choosing data.
<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube6.png width="650" alt="cube6"/>

You can see the numbers by clicking the graph.

<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube7.jpg width="550" alt="cube7"/>

### 3. POP Analysis Tool
[POP](https://apps.fz-juelich.de/scalasca/releases/cube/4.5/docs/guide/html/AdvisorPOPAnalysis.html) is the a automated tool inside CUBE that can give you scores of reference to better evaluate the data.

Attempting to optimize the performance of a parallel code can be a daunting task, and often it is difficult to know where to start. For example, we might ask if the way computational work is divided is a problem? Or perhaps the chosen communication scheme is inefficient? Or does something else impact performance? To help address this issue, POP has defined a methodology for analysis of parallel codes to provide a quantitative way of measuring relative impact of the different factors inherent in parallelization.

The score is computed in the following way (Accoring to the Official Web):

<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube8.png width="850" alt="cube8"/>

To see the socre, you can click the `General` in right side bar and choose `automatic`

<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube9.png width="850" alt="cube9"/>

In the Tag Bar, click the `Scpre-P Configuration` you can see the detail configuration of Score-P.
<img src=https://github.com/jliagouris/ccproject/blob/master/Images/cube10.jpg width="850" alt="cube10"/>
