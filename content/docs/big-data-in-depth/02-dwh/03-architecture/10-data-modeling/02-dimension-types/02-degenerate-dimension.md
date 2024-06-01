---
title: Degenerated Dimension
linktitle: Degenerated Dimension
weight: 62

toc: true
type: docs
date: 2020-01-07

draft: false

menu:
  10-data-modeling:
    parent: Dimension Types
    weight: 62
---

[Ch.02: DWH](../../../../../02-dwh) | [DWH Components](../../../../03-architecture/) | [Data Modeling](../../../10-data-modeling/) | [Dimension Types](../../02-dimension-types/)

## Lesson Notes

[Degenerate Dimension Lesson Notes](../02-degenerate-dimension.pdf)


## Video

{{< youtube JeIFe6GsGrc >}}

## Degenerate Dimensions

-   Degenerate Dimensions

    -   Dimension Key without corresponding dimension table.

    -   Stored in fact table.

    -   It used to provide a grouping for business cases.

### Degenerate Dimensions Example

![Degenerate Dimensions Example](../figures/dd-dim.png)

|OrderID | OrderDate | ProductID | Quantity | Amount|
|---|---|---|---|---|
|123 | 123456789 | 111 | 2 | 120.45|
|123 | 123456789 | 222 | 5 | 10.45|
|431 | 98765122 | 333 | 1 | 15.45|
|431 | 98765122 | 555 | 6 | 4.45|

## Further Reading

**Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf). You can read the below parts for more information about degenerate dimension.

- Chapter 5: Dimensional Model Design Life Cycle Section 5.4.2
- Chapter 6.3.1 Degenerate dimensions page 240

## Previous Chapters

[Overview](../../../../../../big-data-in-depth/)  | [Ch.01: Intro](../../../../../01-introduction) 
