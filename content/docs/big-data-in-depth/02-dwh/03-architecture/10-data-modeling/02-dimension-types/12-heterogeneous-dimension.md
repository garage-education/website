---
title: Heterogeneous Dimension
linktitle: Heterogeneous Dimension
weight: 73

toc: true
type: docs
date: "2020-01-07T00:00:00+01:00"

draft: false

menu:
  10-data-modeling:
    parent: Dimension Types
    weight: 73
---

[Ch.02: DWH](../../../../../02-dwh) | [DWH Components](../../../../03-architecture/) | [Data Modeling](../../../10-data-modeling/) | [Dimension Types](../../02-dimension-types/)

## Lesson Notes

Heterogeneous Dimension Lesson Notes:
1. [Presentation Mode](../12-heterogeneous-dimension-ps.pdf)
1. [Static Mode](../12-heterogeneous-dimension-rs.pdf)


## Video

{{< youtube WJypmDJkAyM >}}

## Heterogeneous Dimensions

-   This type works when we have a case that a company selling different
    product to the same base of customer. Every product has it different
    attributes.

-   One famous example of this type assume an insurance company has two
    types of product like health and car. In this case Car insurance has
    different attributes than the health insurance.

-   If we tried to model this two different products this type name
    Heterogeneous dimensions.

### Heterogeneous Dimensions

-   There are different scenario to implement this type

    **Separate Dimensions**: Split each one in separate dimensions and facts. It will be less
        data and business will do this analysis from two separate facts.

    **Merge Attributes**: We will merge all the attributes in one single table and we will
        add the common attributes and null for un related attributes.
        Implementing this scenarios when we have less different of
        attributes. However, this implementation is not recommended
        because of the table size, performance, and maintenance.

    **Generic Design**: In this approach we will create a single fact table and single
        dimension with the common attributes. The problem of this design
        we will report or care about the common attributes only.

## Further Reading

**Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf). You can read the following:

- Chapter 6.3.12 Heterogeneous products* page 292

## Previous Chapters

[Overview](../../../../../../big-data-in-depth/)  | [Ch.01: Intro](../../../../../01-introduction) 

