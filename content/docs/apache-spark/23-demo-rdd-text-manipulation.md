---
title: "Demo: RDD Text Manipulation"
weight: 23
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Demonstrate text manipulation using RDDs in Spark.
- Learn how to apply transformations and actions on text data.
- Explore practical examples of RDD operations for text processing.

## DEMO

### Example: Text Manipulation RDD

```python
text = ["Hello Spark", "Hello Scala", "Hello World"]
text_rdd = sc.parallelize(text)
print(f"Original Text RDD result: {text_rdd.take(10)}")

```

```python

words_rdd = text_rdd.flatMap(lambda line: line.split(" "))
print(f"Words RDD result: {words_rdd.take(10)}")

```

```python

upper_words_rdd = words_rdd.map(lambda word: word.upper())
print(f"Upper Words RDD result: {upper_words_rdd.take(10)}")

```

## Watch on Youtube

{{< youtube zGvYGJNTfvs >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-23-Demo-RDD-Text-Manipulation.mp4" controls="yes" >}}

You can download the video by right clicking the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-23-Demo-RDD-Text-Manipulation.mp4)


## Download the code

You can download the Jupyter notebook, Databricks Notebook, or the Python source code using the following links:

- [Jupyter Notebook `.ipynb`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/23-spark-text-manipulation/23-spark-text-manipulation.ipynb)
- [Databricks Notebook `.dbc`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/23-spark-text-manipulation/23-spark-text-manipulation.dbc)
- [Python Source Code `.py`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/23-spark-text-manipulation/23-spark-text-manipulation.py)
