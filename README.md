# COMP 6908-Database


## Checklist

+ [ ] relAlg.py
    - [ ] select function
        -  [x] baseline (the = operator is finished)
        -  [ ] < operator
        -  [ ] <= operator
        -  [ ] \> operator
        -  [ ] \>= operator
        -  [ ] print the total number of pages read from B+ tree or from data files
    - [x] project function
    - [ ] join function
        -  [x] baseline
        -  [ ] use B+ tree or nested-loops-page-at-a-time to join
+ [ ] buildTree.py
    - [x] function to build b+ tree index
    - [x] assign pages to tree node and data records
    - [x] store tree index to actual txt files
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
