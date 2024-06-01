---
title: Junk Dimension
linktitle: Junk Dimension
weight: 63

toc: true
type: docs
date: 2020-01-07

draft: false

menu:
  data-modeling:
    parent: Data Modeling
    weight: 63
---

[Ch.02: DWH](../../../../../02-dwh) | [DWH Components](../../../../03-architecture/) | [Data Modeling](../../../10-data-modeling/) | [Dimension Types](../../02-dimension-types/)

## Lesson Notes

[Garbage (Junk) Dimensions Lesson Notes](../03-junk-dimension.pdf)

## Video

{{< youtube S6JleQIpj2g >}}

## Junk Dimension

-   It used to reduce the number of dimensions (low-cardinality columns)
    in the dimensional model and reduce the number of columns in the
    fact table. It is a collection of random transnational codes, flags,
    or text attributes.

-   It optimizes space as fact tables should not include low-cardinality
    or text fields. It mainly includes measures, foreign keys, and
    degenerate dimension keys.

### Junk Dimension Example

![Junk Without Dimensions Example](../figures/junk-dim-ex-without.png)

![Junk Dimensions Example](../figures/junk-dim-ex.png)

### Junk Dimension Table Size

-   We must split the Junk dimension into more dimensions in case the
        size grows by the time.
    
-   It is easy to calculate the expected number of rows as it is the
        total number of combinations between the low-cardinality attributes;
        3 columns each have 3 values total = 3 \* 3 = 9.

## Further Reading

- Chapter 6.3.8 Identifying Garbage (Junk) Dimensions page 282 from **Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf).


## Previous Chapters

[Overview](../../../../../../big-data-in-depth/)  | [Ch.01: Intro](../../../../../01-introduction) 
