---
title: "Demo: Repartition Vs. Coalesce"
weight: 27
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Explain in detail the difference between repartition and coalesce in Spark RDD APIs.
- Analyze the Spark source code implementation for repartition and coalesce to understand their differences.
- Demonstrate practical examples of how to use repartition and coalesce functions in Spark.

## DEMO

### `repartition` Vs. `coalesce` Function

```python
from pyspark.sql.functions import col, expr
import random
import string
from datetime import datetime, timedelta

# Function to generate random log entry
def generate_log_entry():
  user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
  action = random.choice(["login", "logout", "purchase", "click", "view"])
  item_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
  timestamp = (datetime.now() - timedelta(seconds=random.randint(0, 2592000))).strftime("%Y-%m-%d %H:%M:%S")
  return (user_id, action, item_id, timestamp)

# Generate synthetic data
log_entries = [generate_log_entry() for _ in range(1000000)]

# Create DataFrame
columns = ["user_id", "action", "item_id", "timestamp"]
log_df = spark.createDataFrame(log_entries, columns)

# Show sample data
log_df.show(10, truncate=False)

# Save to a CSV file in the DBFS (Databricks File System)
log_df.write.csv("/tmp/user_logs", header=True, mode="overwrite")

```

### `repartition` Function

```python
# 10. repartition
#https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/rdd/RDD.scala#L480
print("\n### 10. repartition ###")
print("Description: Return a new RDD that has exactly numPartitions partitions.")

logs_rdd = sc.textFile("/tmp/user_logs")

# Initial number of partitions
initial_partitions = logs_rdd.getNumPartitions()
print(f"Initial Partitions: {initial_partitions}")

# Repartition to 200 partitions
repartitioned_rdd = logs_rdd.repartition(100)
new_partitions = repartitioned_rdd.getNumPartitions()
print(f"New Partitions after Repartition: {new_partitions}")

```

### `coalesce` Function

```python
# 11. coalesce
print("\n### 11. coalesce ###")
print("Description: Return a new RDD that is reduced into numPartitions partitions.")
#https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/rdd/RDD.scala#L506
#https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/rdd/CoalescedRDD.scala
# Initial number of partitions
initial_partitions = logs_rdd.getNumPartitions()
print(f"Initial Partitions: {initial_partitions}")

# Coalesce to 4 partitions
coalesced_rdd_1 = logs_rdd.coalesce(2)
new_partitions_1 = coalesced_rdd_1.getNumPartitions()
print(f"new_partitions_1 after Coalesce: {new_partitions_1}")

# Coalesce to 50 partitions
coalesced_rdd_2 = logs_rdd.coalesce(10)
new_partitions_2 = coalesced_rdd_2.getNumPartitions()
print(f"new_partitions_2 after Coalesce: {new_partitions_2}")

```


## Watch on Youtube

{{< youtube u4GOzW01tNA >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-27-Demo-Repartition-Vs-Coalesce.mp4" controls="yes" >}}

You can download the video by right clicking the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-27-Demo-Repartition-Vs-Coalesce.mp4)


## Download the code

You can download the Jupyter notebook, Databricks Notebook, or the Python source code using the following links:

- [Jupyter Notebook `.ipynb`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/27-repartition-vs-coalesce/repartition-vs-coalesce.ipynb)
- [Databricks Notebook `.dbc`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/27-repartition-vs-coalesce/repartition-vs-coalesce.dbc)
- [Python Source Code `.py`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/27-repartition-vs-coalesce/repartition-vs-coalesce.py)
