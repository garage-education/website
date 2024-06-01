---
title: Conformed Dimension
linktitle: Conformed Dimension
weight: 61

toc: true
type: docs
date: "2020-01-07T00:00:00+01:00"

draft: false

menu:
  data-modeling:
    parent: Data Modeling
    weight: 61
---

[Ch.02: DWH](../../../../../02-dwh) | [DWH Components](../../../../03-architecture/) | [Data Modeling](../../../10-data-modeling/) | [Dimension Types](../../02-dimension-types/)

## Lesson Notes

[Conformed Dimension Lesson Notes](../01-conformed-dimension.pdf)


## Video

{{< youtube g4O6k75lfKQ >}}

## Conformed Dimensions

Conformed Dimensions: the dimension which is and has the across many fact tables which it
    relates and used in different areas of the warehouse.

- **Date as a Key**: if we have a date column across many facts, we could use the
        date as key in all tables. So, it should be a unified format.

- **Product-Id as a Key**: if we have a product name which could vary between systems
ex: (upper/lower) We can create a dimension table for the product
        details and use product id unified across fact tables.


## Further Reading

- Chapter 5: Dimensional Model Design Life Cycle Section 5.4.3 from **Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf).


## Previous Chapters

[Overview](../../../../../big-data-in-depth/)  | [Ch.01: Intro](../../../../../01-introduction) 
