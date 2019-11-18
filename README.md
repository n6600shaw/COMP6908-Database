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
        -  [ ] fix the bug: one index value corresponds to multiple data files
    - [x] project function
        -  [x] read from multiple pages
    - [ ] join function
        -  [x] baseline
        -  [ ] use B+ tree or nested-loops-page-at-a-time to join
+ [x] buildTree.py
    - [x] function to build b+ tree index
    - [x] assign pages to tree node and data records
    - [x] store tree index to actual txt files
+ [ ] remove.py
    - [x] removeTree function
        -  [x] baseline
        -  [x] release the occupied pages to the page pool
        -  [ ] test remove tree function on real tree files generated
    - [x] removeTable function
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

