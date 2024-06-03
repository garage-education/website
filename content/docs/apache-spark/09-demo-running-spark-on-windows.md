---
title: "Demo: Running Spark on Windows"
weight: 9
menu: apache-spark
date: 2024-06-01
---

## Lesson objectives
In this lesson, we will explain the following topics:
- Demonstrate the process of installing and running Spark on Windows.
- Understand the configuration steps required for Spark installation on Windows.
- Explore the execution of Spark applications on a Windows environment.

## Install Apache Spark on Windows

1. Install Java Development Kit (JDK):
    - Download OpenJDK from the [Adoptium website](https://adoptium.net/en-GB/temurin/releases/?os=windows&version=11).
    - Install JDK and set the `JAVA_HOME` environment variable.

2. Download Spark:
    - Go to the [Apache Spark website](https://spark.apache.org/downloads.html).
    - Choose a Spark release (e.g., 3.4.3) and a package type (e.g., pre-built for Apache Hadoop 3.3).
    - Download and extract the package to a directory (e.g., `C:\spark`).

3. Set Environment Variables:
    - Add Spark’s `bin` directory to the system `PATH`. For example, add `C:\spark\bin` to the PATH variable.
    - Set `HADOOP_HOME` if required (e.g., `C:\hadoop`).

4. Install WinUtils:
    - Download `winutils.exe` from (https://github.com/robguilarr/spark-winutils-3.3.1/blob/master/hadoop-3.3.1/bin/winutils.exe).
    - Place `winutils.exe` in the `bin` directory of Hadoop (e.g., `C:\hadoop\bin`).

5. Verify Installation:
    - Open a command prompt.
    - Type `spark-shell` and press Enter.
    - The Spark shell should start, confirming the installation.

By following these steps, you will have Apache Spark installed on your Windows system.

## Watch on Youtube

{{< youtube KYU_yq3ESXE >}}

## Watch on our Servers

{{< video src="https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-09-Demo-Running-Spark-on-Windows.mp4" controls="yes" >}}

You can download the videog the link and chose save link as: [Download Video](https://dn8min85zvx9p.cloudfront.net/spark-course/Ch.04-09-Demo-Running-Spark-on-Windows.mp4)
