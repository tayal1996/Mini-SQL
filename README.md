**Programming Languages Allowed : Java, Python and C/C++
Dataset:**

1. csv files for tables.
    a. If a file is : ​ File1.csv ​ , the table name would be File
    b. There will be no tab ​ separation or space ​ separation, so you are not required
       to handle it but you have to make sure to take care of both csv file type
       cases: the one where values are in double quotes and the one where values
       are without quotes.
2. All the elements in files would be ​only INTEGERS​
3. A file named: ​ metadata.txt​ (note the extension) would be given to you which will
    have the following structure for each table:
       <begin_table>
       <table_name>
          <attribute1>
             ....
          <attributeN>
<end_table>
**Type of Queries:** ​​ ​ You’ll be presented with the following set of queries:
1. Select all records :
Select * from table_name;
2. Aggregate functions: Simple aggregate functions on a single column.
Sum, average, max and min. They will be very trivial given that the data is only
numbers:
Select max(col1) from table1;
3. Project Columns(could be any number of columns) from one or more tables :
Select col1, col2 from table_name;


4. Select/project with distinct from one table: (distinct of a pair of values indicates the
    pair should be distinct)
       Select distinct col1, col2 from table_name;
5. Select with where from one or more tables :
    Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;
a. In the where queries, there would be a maximum of one AND/OR operator
with no NOT operators.
b. Relational operators that are to be handled in the assignment, the operators
include "< , >, <=, >=, =".
6. Projection of one or more(including all the columns) from two tables with one join
    condition :
       a. Select * from table1, table2 where table1.col1=table2.col2;
       b. Select col1, col2 from table1,table2 where table1.col1=table2.col2;
       c. NO REPETITION OF COLUMNS – THE JOINING COLUMN SHOULD BE
          PRINTED ONLY ONCE.

● For Python it will be – python3 engine.py “select * from table_name where
condition;”
**Format of Output:**
<Table1.column1,Table1.column2....TableN.columnM>
Row
Row


### .......

RowN
