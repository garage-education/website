---
title: "Demo Running Spark On Databricks"
weight: 10
menu: apache-spark
date: 2024-06-01
jupyter:
  jupytext:
    formats: ipynb,md
    main_language: python
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.2
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Demonstrate the process of running Spark on Databricks.
- Understand the benefits of using Databricks for Spark workloads.
- Explore practical examples of Spark applications running on Databricks.

## Introduction To RDD

```python
# Create an RDD from a list of numbers
numbers = [1, 2, 3, 4, 5]
numbers_rdd = sc.parallelize(numbers)
numbers_rdd
```

```python
print(numbers_rdd) 
```

```python
# Apply a transformation: multiply each number by 2
doubled_rdd = numbers_rdd.map(lambda x: x * 2)
```

```python
# Perform an action: collect the results to a list
result = doubled_rdd.collect()

# Print the result
print(result)  # Output: [2, 4, 6, 8, 10]
```

## Spark Lazy Evaluation
```python
# Create an RDD
rdd = sc.parallelize([
    ("John", 28),
    ("Smith", 44),
    ("Adam", 65),
    ("Henry", 23)
])

# Apply a map transformation to create a new RDD with a tuple including the name and a boolean flag
# if the person is older than 30
mapped_rdd = rdd.map(lambda x: (x[0], x[1], x[1] > 30))

# Filter the RDD to include only people older than 30
filtered_rdd = mapped_rdd.filter(lambda x: x[2])

# Convert the filtered RDD back to a DataFrame
df = spark.createDataFrame(filtered_rdd, ["Name", "Age", "OlderThan30"])

# Select only the name and age columns
final_df = df.select("Name", "Age")

# # Collect the results which triggers the execution of all transformations
results = final_df.collect()
display(results)
```

## Watch on Youtube

{{< youtube fU6PZAc8h1I >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-10-Demo-Running-Spark-on-Databricks.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-10-Demo-Running-Spark-on-Databricks.mp4)

