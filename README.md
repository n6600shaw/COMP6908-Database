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
    - [x] select function
        -  [x] scan data from B+Tree or data files
        -  [x] via clustered index (including operator: <, <=, =, \>, \>=)
        -  [x] via unclustered index (including operator: <, <=, =, \>, \>=)
        -  [x] print the total number of pages read from B+ tree or from data files
        -  [x] fix the bug: one index value corresponds to multiple data files
    - [x] project function
        -  [x] read from multiple pages
    - [ ] join function
        -  [x] baseline
        -  [x] use nested-loops-page-at-a-time to join
        -  [ ] use B+ tree to join
+ [x] buildTree.py
    - [x] function to build b+ tree index
    - [x] assign pages to tree node and data records
    - [x] store tree index to actual txt files
+ [x] remove.py
    - [x] removeTree function
        -  [x] baseline
        -  [x] release the occupied pages to the page pool
        -  [x] test remove tree function on real tree files generated
    - [x] removeTable function
+ [x] display.py
    - [x] displayTree function
        -  [x] baseline
        -  [x] save to the appropriate file
    - [x] displayTable function
        -  [x] baseline
        -  [x] display as the required format
+ [x] query.py
    - [x] query a
    - [x] query b
    - [x] query c
    - [x] query d
    - [x] query e

