---
title: "Demo Running Spark On Databricks"
weight: 10
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives

In this lesson, we will explain the following topics:
- Demonstrate the process of running Spark on Databricks.
- Understand the benefits of using Databricks for Spark workloads.
- Explore practical examples of Spark applications running on Databricks.


## Apache Spark Installation on macOS

### 1. Install Homebrew (if not already installed)
Homebrew is a package manager for macOS. If you don't have it installed, you can install it using:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Follow the on-screen instructions to complete the installation.

### 2. Install Java
Apache Spark requires Java. Install OpenJDK using Homebrew:
```bash
brew install openjdk@11
```
Add OpenJDK to your PATH:
```bash
echo 'export PATH="/usr/local/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
Verify the installation:
```bash
java -version
```

### 3. Download Apache Spark 3.4.3
Go to the [Apache Spark download page](https://spark.apache.org/downloads.html) and download the Spark 3.4.3 pre-built for Hadoop 3.3 and later. Alternatively, you can use the following `wget` command:
```bash
wget https://archive.apache.org/dist/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz
```

### 4. Extract the Spark tar file
Extract the downloaded tar file:
```bash
tar xvf spark-3.4.3-bin-hadoop3.tgz
```

### 5. Move Spark to the installation directory
Move the extracted Spark folder to `/usr/local/spark`:
```bash
sudo mv spark-3.4.3-bin-hadoop3 /usr/local/spark
```

### 6. Set up environment variables
Open your `.zshrc` file (or `.bashrc` if you are using bash):
```bash
nano ~/.zshrc
```
Add the following lines at the end:
```bash
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
Save and close the file. Then, apply the changes:
```bash
source ~/.zshrc
```

## 7. Start Spark
To start the Spark shell, you can run:
```bash
spark-shell
```

## Watch on Youtube

{{< youtube fU6PZAc8h1I >}}

## Watch on our Servers

{{< video src="https://garage-education.s3.amazonaws.com/spark-course/Ch.04-10-Demo-Running-Spark-on-Databricks.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://garage-education.s3.amazonaws.com/spark-course/Ch.04-10-Demo-Running-Spark-on-Databricks.mp4)
