---
title: "Demo: Immutability In Spark"
weight: 22
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Demonstrate the concept of immutability in Spark.
- Understand how Spark ensures immutability and its impact on data processing.
- Explore practical examples of immutable operations in Spark.

## DEMO
###Immutable RDDs

```python
#Test Immutable RDDs
numbers = [1, 2, 3, 4, 5]
numbers_rdd = sc.parallelize(numbers)
print(f"Original RDD ID: {numbers_rdd.id()}")
print(f"Original RDD ID: {numbers_rdd.id()}")

#Apply a transformation: multiply each number by 2
transformed_rdd = numbers_rdd.map(lambda x: x * 2)
print(f"Transformed RDD ID: {transformed_rdd.id()}")

#Collect the results to trigger the computation
result = transformed_rdd.collect()
print(f"Transformed RDD result: {result}")

```

```scala
// Test Immutable RDDs
val numbers = List(1, 2, 3, 4, 5)
val numbersRdd = sc.parallelize(numbers)
println(s"Original RDD ID: ${numbersRdd.id}")
println(s"Original RDD ID: ${numbersRdd.id}")
println(s"Original RDD ID: ${numbersRdd.id}")


```

```scala
// numbersRdd = numbersRdd.map(x => x * 2) //OPS!!!!!!!!!!!

// Apply a transformation: multiply each number by 2
val transformedRdd = numbersRdd.map(x => x * 2)
println(s"Transformed RDD ID: ${transformedRdd.id}")

// Collect the results to trigger the computation
val result = transformedRdd.collect()
println(s"Transformed RDD result: ${result.mkString(", ")}")
```

```python
#PartRDD -> RDD[ (integer, Part)]
#PartSuppRDD -> RDD [ (integer, PartSupp)]
#JoinedRDD -> RDD [(integer,(Part,PartSupp)) ]
#Perform inner join on part and partsupp datasets
part_joined_partsupp = part_transformed.join(partsupp_mapped)

#Take the first 10 elements of the joined RDD and print them
#for record in part_joined_partsupp.take(10):
#    print(record)

#Print the count of joined records
print(f"Number of joined records = {part_joined_partsupp.count()}")
```

###Immutable DF Example

```python
#Create an RDD
data = [("John", 28), ("Smith", 44), ("Adam", 65), ("Henry", 23)]
rdd = sc.parallelize(data)

#Show the original RDD
print("Original RDD:")
for row in rdd.collect():
  print(row)

```

```python

print(f"Original RDD ID: {rdd.id()}")

rdd = rdd.filter(lambda x: x[1] > 30)

print(f"Original RDD ID After filter: {rdd.id()}")

###Filter rows where the age is greater than 30
filtered_rdd = rdd.filter(lambda x: x[1] > 30)
print(f"Transformed RDD ID: {filtered_rdd.id()}")

###Show the transformed RDD
print("Filtered RDD:")
for row in filtered_rdd.collect():
  print(row)
```

```scala
  // Create an RDD
  val data = Seq(("John", 28), ("Smith", 44), ("Adam", 65), ("Henry", 23))
  val rdd = sc.parallelize(data)

  // Show the original RDD
  println("Original RDD:")
  rdd.collect().foreach(println)
  //rdd = rdd.filter{ case (name, age) => age > 30 }
  // // Filter rows where the age is greater than 30
  val filteredRdd = rdd.filter{ case (name, age) => age > 30 }
  println(s"Transformed RDD ID: ${filteredRdd.id}")

  // Show the transformed RDD
  println("Filtered RDD:")
  filteredRdd.collect().foreach(println)
```

###Spark Lazy Evaluation 

```python
###Create an RDD
rdd = sc.parallelize([
  ("John", 28),
  ("Smith", 44),
  ("Adam", 65),
  ("Henry", 23)
])

#Apply a map transformation to create a new RDD with a tuple including the name and a boolean flag
#if the person is older than 30
mapped_rdd = rdd.map(lambda x: (x[0], x[1], x[1] > 30))

#Filter the RDD to include only people older than 30
filtered_rdd = mapped_rdd.filter(lambda x: x[2])

#Convert the filtered RDD back to a DataFrame
df = spark.createDataFrame(filtered_rdd, ["Name", "Age", "OlderThan30"])

#Select only the name and age columns
final_df = df.select("Name", "Age")

#Collect the results which triggers the execution of all transformations
results = final_df.collect()
display(results)

```


## Watch on Youtube

{{< youtube P0PGbRYHCYQ >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-22-Demo-Immutability-In-Spark.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Videos/Ch.04-22-Demo-Immutability-In-Spark.mp4)


## Download the code

You can download the Jupyter notebook, Databricks Notebook, or the Python source code using the following links:

- [Jupyter Notebook `.ipynb`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/22-spark-immutability/22-spark-immutablility-example.ipynb)
- [Databricks Notebook `.dbc`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/22-spark-immutability/22-spark-immutablility-example.dbc)
- [Python Source Code `.py`](https://dn8min85zvx9p.cloudfront.net/spark-course/Code/22-spark-immutability/22-spark-immutablility-example.py)
