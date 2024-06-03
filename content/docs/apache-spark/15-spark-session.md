---
title: Spark Session
weight: 15
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Understand the concept and purpose of a SparkSession.
- Learn how to create and use a SparkSession in a Spark application.
- Explore the benefits of SparkSession for simplifying Spark interactions and configurations.

## Spark Distributed Execution: SparkSession

### What is a Session?

- A session refers to an interaction between two or more entities.
- In computing, it's especially common in networked computers on the internet.

### Types of Sessions in Computing

- TCP session: A basic form of interaction in network communication.
- Login session: The period when a user is logged into a system.
- HTTP session: A series of interactions between a web server and a client.
- User session: The time a user interacts with a software application.

### Introducing SparkSession

- Similar to the sessions mentioned, Spark has its own SparkSession.
- SparkSession provides a unified entry point to Spark's functionalities.

### Functionality of SparkSession

- **SparkSession:** An object that provides a point of entry to interact with underlying Spark functionality.
- It allows programming Spark with its APIs.
- In an interactive Spark shell, the Spark driver instantiates a SparkSession for you.
- In a Spark application, you create a SparkSession object yourself.
- You can program Spark using DataFrame and Dataset APIs through SparkSession.
- In Scala and Python, the variable is available as `spark` when you start the console.

### SparkSession

- The SparkSession instance is the way Spark executes user-defined manipulations across the cluster.
- There is a one-to-one correspondence between a SparkSession and a Spark Application.
- It connects the Spark driver program with the cluster manager.
- SparkSession determines the resource manager (YARN, Mesos, or Standalone) for communication.
- It allows configuration of Spark parameters.

### Interacting with Spark in Earlier Versions

- In earlier versions of Spark, setting up a Spark application required creating a SparkConf and SparkContext.

```python
# Create SparkContext in old Spark versions
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

sparkConf = SparkConf().setAppName("SparkSessionExample").setMaster("local")
sc = SparkContext(conf=sparkConf)
sqlContext = SQLContext(sc)
```

```scala
// Create SparkContext in old Spark versions
//set up the spark configuration and create contexts
val sparkConf = new SparkConf().setAppName("SparkSessionZipsExample").setMaster("local")
val sc = new SparkContext(sparkConf)
sc.set("spark.some.config.option", "some-value")
val sqlContext = new org.apache.spark.sql.SQLContext(sc)
```

### Simplification in Spark 2.0 with SparkSession

- Spark 2.0 introduced SparkSession, simplifying the way you interact with Spark.
- SparkSession encapsulates SparkConf, SparkContext, and SQLContext.

```python
# Pyspark: Create SparkSession
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSessionExample") \
    .config("spark.some.config.option", "value") \
    .getOrCreate()
```

```scala
// Spark: Create SparkSession
// Create a SparkSession. No need to create SparkContext.
val warehouseLocation = "file:${system:user.dir}/spark-warehouse"
val spark = SparkSession
    .builder()
    .appName("SparkSessionZipsExample")
    .config("spark.sql.warehouse.dir", warehouseLocation)
    .enableHiveSupport()
    .getOrCreate()
```

### Using SparkSession

- Spark 2.0 introduces SparkSession.
- With SparkSession, you can access all Spark functionalities.
- A unified entry point to Spark's functionality, reduces the need for multiple context initializations.
- Encapsulates the functionalities of SQLContext, HiveContext, and more.

### Reference

- The examples shown are based on a blog post from Databricks.
- URL: [https://www.databricks.com/blog/2016/08/15/how-to-use-sparksession-in-apache-spark-2-0.html](https://www.databricks.com/blog/2016/08/15/how-to-use-sparksession-in-apache-spark-2-0.html)

## Watch on Youtube

{{< youtube ABomIh_Z0cQ >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-15-Spark-Session.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-15-Spark-Session.mp4)
