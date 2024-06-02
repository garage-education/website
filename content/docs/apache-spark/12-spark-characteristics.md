---
title: Spark Characteristics
weight: 12
menu: apache-spark
date: 2024-06-01
---
## Lesson objectives

In this lesson, we will explain the following topics:
- Learn about the key characteristics of Spark, including speed, ease of use, modularity, and extensibility.
- Understand how Spark achieves its high performance through hardware utilization, DAG scheduling, and the Tungsten execution engine.
- Explore the benefits of Spark's modular and extensible architecture.

## Spark Characteristics

### Spark Characteristics

- Speed.
- Ease of use.
- Modularity.
- Extensibility.

### Spark Characteristics: Speed

- Spark's speed is achieved through various strategies.
  - **Hardware Utilization:** Spark leverages commodity hardware with extensive memory and multiple cores, utilizing efficient multithreading and parallel processing for improved performance.
  - **Directed Acyclic Graph (DAG):** Spark constructs computations as a DAG. Its scheduler and optimizer create an efficient graph, allowing parallel task execution across cluster workers. *This topic will be discussed later.*

### Spark Characteristics: Speed

- Spark's speed is achieved through various strategies.
    - **Tungsten Execution Engine:** Tungsten enhances Spark's speed by optimizing memory management, shifting from JVM-managed objects to direct binary processing, and employing cache-optimized algorithms and advanced code generation. These improvements reduce CPU and memory bottlenecks, significantly boosting performance. *This topic will be discussed later.*

### Spark Characteristics: Ease of use

- Spark simplifies big data processing with an abstraction called a Resilient Distributed Dataset (RDD).
- RDDs serve as the foundation for higher-level data structures like DataFrames and Datasets in Spark. *This topic will be discussed later.*
- Compared with MapReduce and other complex distributed processing frameworks, Spark provides a simple programming model with a range of transformations and actions.

### Spark Characteristics: Modularity

- Spark operations are flexible, supporting various workloads and languages: Scala, Java, Python, SQL, and R.
- It provides unified libraries with comprehensive APIs (SparkSQL, Structured Streaming, MLlib, and GraphX).
- These modules allow Spark to handle different workloads under a single engine.
- With Spark, you can develop a single application for diverse tasks without the need for separate engines or learning different APIs, achieving a unified processing framework.

### Spark Characteristics: Extensibility

- Spark focuses on its fast, parallel computation engine rather than on storage (Unlike Apache Hadoop, which included both storage and compute).

### Spark Characteristics: Extensibility

- Spark can process data from various sources like Hadoop, Cassandra, HBase, MongoDB, Hive, RDBMSs, and others in memory for faster processing.
- Spark's `DataFrameReader`s and `DataFrameWriter`s allow Spark to interact with even more data sources, such as Kafka, Kinesis, Azure Storage, and Amazon S3.
- The Spark community maintains a list of third-party packages, enhancing its ecosystem with connectors for external data sources, performance monitors, and more.

## Watch on Youtube

{{< youtube KNHZoKgAqXw >}}

## Watch on our Servers

{{< video src="https://garage-education.s3.amazonaws.com/spark-course/Ch.04-12-Spark-Characteristics.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-12-Spark-Characteristics.mp4)
