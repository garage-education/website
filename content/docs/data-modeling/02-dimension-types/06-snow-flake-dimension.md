---
title: Snowflake Dimension
linktitle: Snowflake Dimension
weight: 66

toc: true
type: docs
date: 2020-01-07

draft: false

menu:
  data-modeling:
    parent: Data Modeling
    weight: 66
---

## Lesson Notes

[Snowflake Dimension Lesson Notes](../06-snow-flake-dimension.pdf)


## Video

{{< youtube To_1XQabp0k >}}


## Snowflake Dimensions

-   Snowflake Dimension is a dimension that has a hierarchy of
    attributes. This attribute is normalized, and each dimension has a
    relationship with another hierarchy dimension table.

-   This dimension design not recommended as it has much complexity to the model and query performance. Also, it complicates the ETL process and makes too many dimensions without needs

### Snowflake Dimensions Example

![Snowflake Dimensions Example](../figures/snowflake-dim.png)

## Further Reading

**Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf). You can read the following parts for more information about snowflake dimension.

- Chapter 5: Dimensional Model Design Life Cycle Section 5.4.8
- Chapter 6.3.7: Identifying dimensions that need to be snowflaked page 277
