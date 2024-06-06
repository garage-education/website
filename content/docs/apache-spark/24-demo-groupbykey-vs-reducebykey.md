---
title: "Demo: GroupByKey Vs. ReduceByKey"
weight: 24
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Compare the differences between groupByKey and reduceByKey in Spark.
- Understand the performance implications of each operation.
- Explore practical examples to illustrate the use cases and benefits of both operations.

## DEMO

### Aggregation: groupByKey V. reduceByKey

```python

# Example 3: Group By Transformation
pairs_rdd = sc.parallelize([("A", 1), ("B", 1), ("A", 2), ("B", 2), ("A", 3)] * 5000000)
print(f"Original Pairs RDD result: {pairs_rdd.take(10)}")

```

```python
import time
# Measure performance of groupByKey and sum
start_time = time.time()
grouped_rdd = pairs_rdd.groupByKey().mapValues(lambda values: sum(values))
grouped_result = grouped_rdd.collect()
group_by_key_duration = time.time() - start_time
print(f"GroupByKey duration: {group_by_key_duration:.4f} seconds")
print(f"Grouped RDD result (sum): {grouped_result[:10]}")  # Display only the first 10 results for brevity
```

```python
# Measure performance of reduceByKey and sum
start_time = time.time()
reduced_rdd = pairs_rdd.reduceByKey(lambda x, y: x + y)
reduced_result = reduced_rdd.collect()
reduce_by_key_duration = time.time() - start_time
print(f"ReduceByKey duration: {reduce_by_key_duration:.4f} seconds")
print(f"Reduced RDD result: {reduced_result[:10]}")  # Display only the first 10 results for brevity
```


## Watch on Youtube

{{< youtube WaYbKVNjme0 >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-24-Demo-GroupByKey-Vs-ReduceByKey.mp4" controls="yes" >}}

You can download the video by right clicking the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-24-Demo-GroupByKey-Vs-ReduceByKey.mp4)
