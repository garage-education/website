---
title: 'Home'
date: 2024-06-01
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: biography
    content:
      username: admin
    design:
      biography:
        style: 'text-align: justify; font-size: 0.8em;'
  - block: cta-image-paragraph
    id: solutions
    content:
      items:
        - title: Apache Spark
          text: Join our Apache Spark course
          feature_icon: bolt
          image: spark-thumbnail-3840-2160.png
          button:
            text: Enroll
            url: /docs/apache-spark/
        - title: Hadoop
          text: Join our Hadoop course
          feature_icon: bolt
          image: thumbnails/hadoop_theory.png
          button:
            text: Enroll
            url: /docs/hadoop/
    design:
      css_class: "bg-gray-100 dark:bg-gray-900"
---
