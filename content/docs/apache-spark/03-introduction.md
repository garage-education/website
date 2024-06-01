---
title: Introduction
weight: 3
menu: apache-spark
date: 2024-06-01
---

## Introduction to Apache Spark

### Introduction to Apache Spark

- Apache Spark was initiated at UC Berkeley in 2009, leading to the publication of [Spark: Cluster Computing with Working Sets](https://www1.icsi.berkeley.edu/pubs/networking/ICSI_sparkclustercomputing10.pdf) in 2010 by Matei Zaharia et al.
- Spark was developed to improve processing efficiency over Hadoop MapReduce, which struggled with iterative tasks because it launched separate jobs and reloaded data for each one. This was particularly important for machine learning algorithms that need multiple data passes.
- Initially, Spark was designed for batch applications, but it quickly expanded to include streaming, SQL analytics, graph processing, and machine learning.

### Apache Spark Development and Milestones

- By 2013, the project had more than 100 contributors, and now it has over 2,000 contributors with more than 39,000 commits. It has been donated to the Apache Software Foundation, guaranteeing its future as a vendor-independent project.
- Key milestones in its development are Spark 1.0 in 2014, Spark 2.0 in 2016, and Spark 3.0 in 2020, highlighting its evolution and broad acceptance.

### Features of Apache Spark

- Apache Spark is a **unified engine** designed for large-scale distributed data processing, either on-premises in data centers or in the cloud.
- Spark provides **in-memory** storage for intermediate computations, making it much faster than Hadoop MapReduce.
- Spark offers rich, composable APIs, for example:
    - Spark SQL: SQL for interactive queries.
    - MLlib: for machine learning over big data and complex computations.
    - Structured Streaming: for stream processing with near real-time data.
    - GraphX: for graph processing.
- **Optimized Execution Engine**: Spark's Catalyst optimizer and `Tungsten execution engine` optimize execution plans and generate efficient code for execution.
- 
{{< youtube MiTOvM85WKk >}}

You can download the video by right clicking the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-03-Introduction.mp4)
