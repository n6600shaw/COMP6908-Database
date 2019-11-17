# COMP 6908-Database


## Analysis

### clustered index

Products.pid

**Suppliers.sid**

Supply.sid

### unclustered index

Products.pname

Products.color

Suppliers.sname

Suppliers.address

**Supply.pid**

Supply.cost

## Checklist

+ [ ] relAlg.py
    - [ ] select function
        -  [x] scan data from B+Tree or data files
        -  [x] via clustered index (including operator: <, <=, =, \>, \>=)
        -  [x] via unclustered index (including operator: <, <=, =, \>, \>=)
        -  [ ] print the total number of pages read from B+ tree or from data files
    - [x] project function
    - [ ] join function
        -  [x] baseline
        -  [ ] use B+ tree or nested-loops-page-at-a-time to join
+ [ ] buildTree.py
    - [x] function to build b+ tree index
    - [ ] assign pages to tree node and data records
    - [ ] store tree index to actual txt files
+ [ ] remove.py
    - [ ] removeTree function
        -  [x] baseline
        -  [ ] release the occupied pages to the page pool
    - [ ] removeTable function
+ [ ] display.py
    - [ ] displayTree function
        -  [x] baseline
        -  [ ] save to the appropriate file
    - [ ] displayTable function
+ [x] query.py
    - [x] query a
    - [x] query b
    - [x] query c
    - [x] query d
    - [x] query e

