---
title: Role Playing Dimension
linktitle: Role Playing
weight: 64

toc: true
type: docs
date: 2020-01-07

draft: false

menu:
  10-data-modeling:
    parent: Dimension Types
    weight: 64
---

[Ch.02: DWH](../../../../../02-dwh) | [DWH Components](../../../../03-architecture/) | [Data Modeling](../../../10-data-modeling/) | [Dimension Types](../../02-dimension-types/)

## Lesson Notes

[Role-playing Dimension Lesson Notes](../04-role-playing-dimension.pdf)


## Video

{{< youtube AoN3wjW57pY >}}

## Role-Playing Dimension

Role-Playing Dimensions (Re-usable Dimension): A single physical dimension helps to reference multiple times in a
    fact table as each reference linking to a logically distinct role
    for the dimension.
### Role-Playing Dimension Example


![Role Playing Example](../figures/role-playing-dim.png)

### Conformed vs Role-Playing Dimension


-   **Conformed** is the same dimension used in different facts and has **the same meaning** ex: CustomerID.

-   **Role-Playing** is the same dimension which used multiple times
    within the same fact but **with different meanings** ex: Date.

## Further Reading

- Chapter 6.3.9 Role-playing dimensions page 285 from **Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf).


## Previous Chapters

[Overview](../../../../../../big-data-in-depth/)  | [Ch.01: Intro](../../../../../01-introduction) 
