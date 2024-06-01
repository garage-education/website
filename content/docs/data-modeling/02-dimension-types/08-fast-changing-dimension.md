---
title: Fast Changing Dimension
linktitle: Fast Changing Dimension
weight: 68

toc: true
type: docs
date: 2020-01-07

draft: false

menu:
  data-modeling:
    parent: Data Modeling
    weight: 68
---
## Lesson Notes

Fast Changing Dimension Lesson Notes:
1. [Presentation Mode](../08-fast-changing-dimension-ps.pdf)
1. [Static Mode](../08-fast-changing-dimension-rs.pdf)


## Video

{{< youtube xWe-IP3ATi0 >}}

## Fast Changing Dimension (Mini Dimension)

-   When we have a dimension with one or more of its attributes changing
    very fast.

-   It causes a performance issue if we tried to handle this case similar SCD Type 2 because of the rapidly changing  in this dimension and the table will includes a lot of rows for this dimension

-   We solve this case by separation the attributes into one or more
    dimensions. This technique also called ***mini-dimensions***.

### Fast Changing Dimension Handling

-   How to handle FCD?

    1. Identify the fast changing columns in dimension.
    2. Split the fast changing columns to a separate junk dimension.
    3. Map the junk dimension with the main dimension using *mini-dimension*
    
- In the following example, we have **Weight & B_pressure** columns are FCD.
    
| Patient\_id | Name | Gender | BirthDate | Weight | B\_Pressure | UpdateDt|
|---|---|---|---|---|---|---|
| 123 | Anna | F | 1968-01-12 | 50 | 110.0 |2019-01-01|
| 123 | Anna | F | 1968-01-12 | 55 | 130.0 |2019-01-07|
| 123 | Anna | F | 1968-01-12 | 59 | 115.0 |2019-01-14|
| 123 | Anna | F | 1968-01-12 | 65 | 120.0 |2019-01-21|

- Split FCD columns from the other column.
    - Static columns
    
    |Patient\_id | Name | Gender | BirthDate |
    |---|---|---|---|		
    |123 | Anna   | F | 1968-01-12 |
    
    - FCD
    
    |Patient\_Key | Weight | B\_Pressure |  
    |---|---|---|  
    |1 | 50 | 110.0|
    |2 | 55 | 130.0|
    |3 | 59 | 115.0|
    |4 | 65 | 120.0| 

   - Patient Mini Dimension*
  
    |Patient\_id  | Patient\_Key |  Start\_Date |  End\_Date|
    |-------------|--------------| -------------| ------------|
    |123          | 1            |  2019-01-01  |  2019-01-07|
    |123          | 2            |  2019-01-07  |  2019-01-14|
    |123          | 3            |  2019-01-14  |  2019-01-21|
    |123          | 4            |  2019-01-21  |  null|

	


![Fast Changing Dimensions Example](../figures/fcd-dim.png)

## Fast Changing Dimension Design Discussion

- Fast changing dimension design came from the need to handle the performance issue when 
we have a fact table that needs to join with a dimension that contains static and fast 
changing columns together.


- The main reason to introduce this design was to help to **enhance the performance** 
for retrieving the information between the Fact and the dimension 
**with minimum data redundancy**.

- If we check the first table in our example, we could think about the frequency of the change 
and the application which we need to handle. In this case, we have three scenarios as following:
    
    - First use case, assume we have a fact named clm_svc_dtl (claim service details) table that 
    needs to get some of the static information from the patient 
    dimension for example: patient gender, age, or just the reference for the patient_id. 
    **In this case, we will join directly with the patient dim on Patient_id**.  
    This case will be very fast as it will be one to one join with one record for each patient.
    
        - clm_svc_dtl
         
         |clm_id | clm_svc_dt | patient_id | clm_type| clm_amount|  
         |---|---|---|---|---|
         |123 | 2020-01-01| 123| 1 | 110.0|
         |245 | 2020-01-01| 123| 1 | 130.0|
         |367 | 2020-01-01| 123| 1 | 115.0|          
        
    - Second use case, assume we have a fact table membr_vst_dtl (member visit detail) that 
    has the transactional data for the patient,  and it needs to get the latest 
    *Weight and Blood Pressure*. 
    **In this case, the fact will include the junk dimension surrogate key and join with the 
    junk dimension to get the values**.
        
        - membr_vst_dtl
        
         |clm_id | vst_dt | Patient\_Key|  
         |--- |--------|---------|
         |123 | 2019-01-01 | 1| 
         |245 | 2019-01-07 | 2| 
         |367 | 2019-01-14 | 3|             
         |367 | 2019-01-21 | 4|
           
    - Third use case, assume we have a fact table membr_rsk_score (member risk_score) that calculates risk score based on 
    Weight and Blood Pressure. This risk score needs to check historical 
    data every day and compare the results with the previous for simple example: 
    assume for each day we get the log of 
    (the difference between current blood pressure minus the previous 
    one plus the same for the Weight).
      **In this case, we will join fact with junk with the mini dimension**. 
      Note: This case is not the normal case to check the historical data every day for all facts.
      So, the requirements to access the start and end date for this fact is not frequent request case.
      
      - membr_rsk_score
      
      |rsk_score | calc_dt | Patient\_Key|               
      |--- |--------|---------|                      
      |0.5 | 2019-01-01 | 1|                         
      |0.6 | 2019-01-07 | 2|                         
      |0.3 | 2019-01-14 | 3|                         
      |0.67 | 2019-01-21 | 4|                         
      
      
      
- Let's analyze the implementation strategies which can handle the above three use cases.

    - Keep the patient dimension as is and join with fact directly. 
    The drawback of this design is that the size of the **patient dimension will be huge, 
    with the redundancy of data** and performance issues when joining between Fact and dimension.
    
    - Split the patient dimension into two-dimension static and FCD.
     This solution has an example below, and it will work, but it has some problems. 
     **So, Let's analyze why we can't remove the junk table and use only the mini-dimension table?**
        * The new dimension which contains the fast changing columns will have a bigger size 
        (for more detail about how to choose the number of junk dimensions per table, 
        please refer to the junk dimension lecture here).
         Now we will have a performance issue when joining between 
         the new dimension and fact table.
        * The new dimension will include some columns which not required for the daily query 
        results (start_data and end_date). These columns will cause to make the new table 
        to be the bigger size and affect the performance.
        * One more issue here if we have a bigger number of the fast changing column 
        the combination (as it is the cartesian product of the junk columns values)
         will make the table records to be bigger.    
                                                                                         
          |Patient\_id  | Patient\_Key| Weight | B\_Pressure |  Start\_Date |  End\_Date|
          |-------------|--------------| -------------| ------------| -------------| ------------|
          |123          | 1            | 50 | 110.0| 2019-01-01  |  2019-01-07|
          |123          | 2            | 55 | 130.0| 2019-01-07  |  2019-01-14|
          |123          | 3            | 59 | 115.0| 2019-01-14  |  2019-01-21|
          |123          | 4            | 65 | 120.0| 2019-01-21  |  null|

- The recommended solution as following
    - Split the patient dimension into three tables:
        * Patient Dimension.
        * Junk Dimension(s).
        * Mini Dimension(s).
    - This solution has some perspectives which we need to clarify it.
        - In case we have multi fast changing columns with lots of combinations,
         we could split it into one or more junk and handle this with one or mini dimension tables.
        - When we need to get the junk dimension information, we join with a smaller table, 
        which will increase the performance as it is fewer table columns and size.
        - In case we need to get the historical data with the date columns, we can still get this 
        information by joining between the fact, junk, and mini-dimension.
          
        - Patient Dimension (static columns)
              
        |Patient\_id | Name | Gender | BirthDate |
        |---|---|---|---|		
        |123 | Anna   | F | 1968-01-12 |
              
        - Junk Dimension
              
        |Patient\_Key | Weight | B\_Pressure |  
        |---|---|---|  
        |1 | 50 | 110.0|
        |2 | 55 | 130.0|
        |3 | 59 | 115.0|
        |4 | 65 | 120.0| 
          
        - Mini Dimension
            
        |Patient\_id  | Patient\_Key |  Start\_Date |  End\_Date|
        |-------------|--------------| -------------| ------------|
        |123          | 1            |  2019-01-01  |  2019-01-07|
        |123          | 2            |  2019-01-07  |  2019-01-14|
        |123          | 3            |  2019-01-14  |  2019-01-21|
        |123          | 4            |  2019-01-21  |  null|
          
## Further Reading

**Dimensional Modeling: In a Business Intelligence Environment**. The book is free, and you can download it from [this link](https://www.redbooks.ibm.com/redbooks/pdfs/sg247138.pdf). You can read the following:

- Chapter 5.4.7 Slowly Changing Dimensions page 162.
- Chapter 6.3.6 Fast Changing dimensions page 269.
