---
title: Shrunken Rollup Changing Dimension
linktitle: Shrunken Changing Dimension
weight: 70

toc: true
type: docs
date: "2020-01-07T00:00:00+01:00"

draft: false

menu:
  data-modeling:
    parent: Data Modeling
    weight: 70
---
## Lesson Notes

Shrunken Rollup Changing Dimension Lesson Notes:
1. [Presentation Mode](../09-shrunken-rollup-dimension-ps.pdf)
1. [Static Mode](../09-shrunken-rollup-dimension-rs.pdf)


## Video

{{< youtube jTk-edbyTWM >}}

## Shrunken Rollup Dimensions

-   Shrunken Rollup dimension is used for developing aggregate (higher
    level of summary) fact tables.

-   It required that the data model has a lower level of granularity.

    -   We have a daily usage fact table, and we need to have a higher level
        of monthly usage. So, we use the monthly dimension to get a summary
        of the daily.
    
    -   We have a daily usage fact table aggregated on area-id, and we need
        to create another summary table aggregated based on city id. So, the
        new grain level here is the new dimension for the city.

### Shrunken Rollup Dimensions Cont.

In this example we use the AreaId and the relation with CityID for shrunken the dimension and do higher level of aggregations.

- Order detail per AreaID

    |OrderDate | AreaID|  TotalOrders|
    |----------|----------|----------|
    |123456789 | 123  |20|
    |123456789 | 123  |30|
    |123456789 | 678  |10|
    |123456789 | 678  |12|
- City and Area relationship dimension

    |AreaID | AreaName    | CityID|
    |----------|----------|----------|
    |123    | Al-Matareya | 1|
    |678    | Ain shams   | 1|
- City dimension

    |CityID | CityName|
    |-------|---------|
    |1      | Cairo|
- Order detail per CityID

    |OrderDate | CityID | TotalOrders|
    |----------|----------|----------|
    |123456789 | 1 | 72|
