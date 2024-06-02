---
title: Spark Execution Mode
weight: 17
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Learn about the different execution modes in Spark, including cluster mode, client mode, and local mode.
- Understand the differences and use cases for each execution mode.
- Explore how to configure and execute Spark applications in various modes.

## Execution Modes

### Execution Modes Overview

- Execution modes define the location of resources when running Spark applications.
- Three modes available:
  1. Cluster mode
  2. Client mode
  3. Local mode

### Cluster Manager Components

![A cluster driver and worker (no Spark Application yet).](../Figures/chapter-04/cluster_manager_processes.png)
*Figure 1: A cluster driver and worker (no Spark Application yet).*

### Cluster Mode

- Most common mode for running Spark Applications.
- User submits a pre-compiled JAR, Python script, or R script to a cluster manager.
- The cluster manager then launches the driver process on a worker node inside the cluster.
- Executor processes also launched within the cluster.
- Cluster manager handles all Spark Application processes.
- This means that the cluster manager is responsible for maintaining all Spark Application–related processes.

### Spark Cluster Mode

![Spark’s cluster mode.](../Figures/chapter-04/spark_cluster_mode.png)
*Figure 2: Spark’s cluster mode.*

### Client Mode

- Similar to cluster mode, but the **Spark driver remains on the client machine that submitted the application**.
- **Client machine** is responsible for maintaining the Spark driver process.
- **Cluster manager** maintains executor processes.
- Commonly used with gateway machines or edge nodes.
- The driver is running on a machine outside of the cluster but that the workers are located on machines in the cluster.

### Spark Client Mode

![Spark’s client mode.](../Figures/chapter-04/spark_client_mode.png)
*Figure 3: Spark’s client mode.*

### Local Mode

- Runs the entire application on a single machine.
- Parallelism achieved through threads on the same machine.
- Ideal for learning, testing, or local development.
- Not recommended for production use.

## Watch on Youtube

{{< youtube Q5EH1rHIdBM >}}

## Watch on our Servers

{{< video src="https://garage-education.s3.amazonaws.com/spark-course/Ch.04-17-Spark-Execution-Mode.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-17-Spark-Execution-Mode.mp4)
