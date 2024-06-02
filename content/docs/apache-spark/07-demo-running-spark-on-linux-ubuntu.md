---
title: "Demo: Running Spark on Linux Ubuntu"
weight: 7
menu: apache-spark
date: 2024-06-01
---


## Lesson objectives

In this lesson, we will explain the following topics:
- Demonstrate the process of installing and running Spark on Linux Ubuntu.
- Understand the configuration steps required for Spark installation on Ubuntu.
- Explore the execution of Spark applications on a Linux environment.

# Apache Spark Installation on Ubuntu

## Docker For testing
```bash
docker pull ubuntu:24.04
docker run -it --name spark-ubuntu-container ubuntu:24.04
apt-get update
apt-get install curl wget
```

## 1. Update the package list
```bash
sudo apt-get update
```

### 2. Install Java
Apache Spark requires Java. Install OpenJDK:
```bash
apt-get install openjdk-11-jdk
```
Verify the installation:
```bash
java -version
```

### 3. Download Apache Spark
Go to the [Apache Spark download page](https://spark.apache.org/downloads.html) and copy the link to the latest release. Use `wget` to download it:
```bash
wget https://archive.apache.org/dist/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz
```

### 4. Extract the Spark tar file
```bash
tar xvf spark-3.4.3-bin-hadoop3.tgz
```

### 5. Move Spark to the installation directory
```bash
mv spark-3.4.3-bin-hadoop3 /opt/spark
```

### 6. Set up environment variables
Open the `.bashrc` file:
```bash
vi ~/.bashrc
```
Add the following lines at the end:
```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
Save and close the file. Then, apply the changes:
```bash
source ~/.bashrc
```


## Watch on Youtube

{{< youtube Oz_3u_NIS2w >}}

## Watch on our Servers

{{< video src="https://garage-education.s3.amazonaws.com/spark-course/Ch.04-07-Demo-Running-Spark-on-Linux-Ubuntu.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-07-Demo-Running-Spark-on-Linux-Ubuntu.mp4)
