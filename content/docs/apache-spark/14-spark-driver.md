---
title: Spark Driver
weight: 14
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Learn about the role and key functions of the Spark driver.
- Understand how the driver schedules and distributes tasks to executors.
- Explore the communication and resource management responsibilities of the driver.

## Spark Driver

The driver is the process `in the driver seat.`[^1] of your Spark Application.

[^1]: Spark: The Definitive Guide, Chapter 15.

### Spark Driver: Key functions

- It transforms all the Spark operations into DAG computations, schedules them, and distributes their execution as tasks across the Spark executors.
- Controlling the execution of a Spark Application.

### Spark Driver: Key functions

- Acting as a process on a physical machine, responsible for the overall state of the application on the cluster.
- It instantiates the `SparkSession`.
- It requests resources (CPU, memory, etc.) from the cluster manager for Spark’s executors (JVMs).
- Once the resources are allocated, it communicates directly with the executors.

### Spark Driver: Recap

![Spark Driver Recap](../Figures/chapter-04/Mairmaid_SparkDriver.png)

## Watch on Youtube

{{< youtube ODcbq13Y1F0 >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-14-Spark-Driver.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-14-Spark-Driver.mp4)
