---
title: Spark Operations
weight: 20
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Understand the two types of Spark operations: transformations and actions.
- Learn about the immutability of Spark operations and its implications.
- Explore examples of transformations and actions, including lazy evaluation and its benefits.

## Spark Operations

### Spark Operations

- Spark **operations** on distributed data can be classified into two types: transformations and actions.
- All spark operations are **immutable**.

### Immutable Objects

- An object whose state cannot change after it has been constructed is called immutable (unchangeable).[^1]
- The methods of an immutable object do not modify the state of the object.

[^1]: Referenced from [https://otfried.org/courses/cs109scala/tutorial_mutable.html](https://otfried.org/courses/cs109scala/tutorial_mutable.html)

### Immutable Objects

![Spark Dataframe is immutable, and you can't change its values.](../Figures/chapter-04/Immutable_df.png)
*Figure 1: Spark Dataframe is immutable, and you can't change its values.*

### Immutable Objects

![Filtering a PySpark DataFrame Based on Age](../Figures/chapter-04/pyspark_immutable_df.jpeg)
*Figure 2: Filtering a PySpark DataFrame Based on Age*

### DEMO

DEMO

### Spark Operations: Transformations

- Transformations: transform a Spark DataFrame into a new DataFrame **without altering the original data**.
- Example of Spark transformations: **map(), select(), filter(), or drop()**.

### Spark Transformations: What are Lazy Transformations?

- In Spark, transformations are **lazy**.
- This means computations are not executed immediately.
- Spark builds a **DAG** (Directed Acyclic Graph) of transformations.
- All Transformations results are not computed immediately, but they are recorded or remembered as a **lineage**.

### Spark Transformations: Benefits of Lazy Evaluation

- **Optimization:** A lineage allows Spark, at a later time in its execution plan, to rearrange certain transformations, coalesce them, or optimize transformations into stages for more efficient execution.
- **Resource Management:** Executes tasks efficiently, using fewer resources.
- **Fault Tolerance:** Easier to recompute parts of the pipeline if a part fails.

### Spark Transformations: Lazy Transformation

- Consider a dataset with map and filter transformations.
- Spark does not execute these transformations when they are defined.
- Transformations are executed when an action (like **collect**, **count**) is called.

### Lazy Transformations Example

![Spark Lazy Transformations Example.](../Figures/chapter-04/pyspark_transformations.jpeg)
*Figure 3: Spark Lazy Transformations Example.*

### Spark Operations: Actions

- An action triggers the lazy evaluation of all the recorded transformations.
- Actions are operations that trigger execution of transformations.
- They are used to either compute a result to be returned to the Spark driver program or to write data to an external storage system.
- Actions include operations like **count**, **collect**, **saveAsTextFile**, and **take**.

### Examples of Spark Actions

- **collect():** Collects all elements from the Spark context to the driver program.
- **count():** Returns the number of elements in the dataset.
- **saveAsTextFile(path):** Saves the dataset to a text file at the specified path.
- **take(n):** Returns an array with the first n elements of the dataset.

## Watch on Youtube

{{< youtube SDcdnkdiM04 >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-20-Spark-Operations.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-20-Spark-Operations.mp4)
