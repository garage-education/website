---
title: From Map Reduce To Spark
weight: 11
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Understand the basic idea and stages of MapReduce.
- Learn about the limitations of MapReduce and the motivation for Spark.
- Explore the improvements offered by Spark over MapReduce, including in-memory processing and optimized execution.

## From MapReduce to Apache Spark

### The basic idea of MapReduce

- Assume we need to launch a high-throughput bulk-production sandwich shop.
- This sandwich has a lot of raw ingredients, and our target is to produce the sandwich as quickly as possible.
- To make the production very quickly we need to distribute the tasks between the *workers*.

*This example taken from [https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/](https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/)*

### The basic idea of MapReduce

We break this into three stages:
- Map.
- Shuffle/Group (Mapper Intermediates).
- Reduce.

*This example taken from [https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/](https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/)*

### Map

We distribute our raw ingredients amongst the workers.

![Map](../Figures/chapter-04/map.png)

*This example taken from [https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/](https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/)*

### Shuffle/Group

We will organise and group the processed ingredients into piles, so that making a sandwich becomes easy.

![Shuffle/Group](../Figures/chapter-04/map_shuffle.png)

*This example taken from [https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/](https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/)*

### Reduce

We’ll combine the ingredients into a sandwich.

![Reduce](../Figures/chapter-04/map_reduce.png)

*This example taken from [https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/](https://reberhardt.com/cs110/summer-2018/lecture-notes/lecture-14/)*

### Map Reduce Bottleneck

![Map Reduce Bottleneck](../Figures/chapter-04/MR.jpg)

### Spark Motivation

- In-Memory Processing.
- Resilient Distributed Datasets (RDDs): Spark uses RDDs to perform parallel operations on data stored across cluster nodes, minimizing disk I/O by keeping data in RAM.
- Optimized Execution (DAG execution engine): The DAG execution engine organizes computations efficiently, reducing unnecessary operations and combining tasks to lower data movement.
- Caching: Spark allows for the caching of intermediate data in memory, benefiting iterative algorithms that reuse data, thereby avoiding repetitive disk access.
- Advanced Optimization (Catalyst optimizer and Tungsten): With components like the Catalyst optimizer and Tungsten for memory and CPU efficiency, Spark streamlines execution, making it ideal for fast, iterative processing over big data.

## Watch on Youtube

{{< youtube uMf8dCcQoBQ >}}

## Watch on our Servers

{{< video src="https://garage-education.s3.amazonaws.com/spark-course/Ch.04-11-From-Map-Reduce-To-Spark.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-11-From-Map-Reduce-To-Spark.mp4)
