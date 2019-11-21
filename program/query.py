import os

from program.relAlg import select, project, join
from program.display import displayTable
from program.remove import removeTree, removeTable

SUPPLY = "Supply"
PRODUCTS = "Products"
SUPPLIERS = "Suppliers"

OUTPUT_PATH = "../queryOutput/"
QUERY_RESULT = "queryResult.txt"


def query_x():
    result = select(SUPPLY, "sid", "<=", "s15")
    return result


def query_a():
    tmp_result = select(SUPPLIERS, "sid", "=", "s23")
    query_result = project(tmp_result, ["sname"])
    removeTable("Suppliers_tmp")
    return query_result


def query_b():
    tmp_result = select(SUPPLIERS, "sid", "=", "s23")
    query_result = project(tmp_result, ["sname"])
    removeTable("Suppliers_tmp")
    return query_result


def query_c():
    tmp_result = select(SUPPLY, "pid", "=", "p15")
    tmp_result = join(SUPPLIERS, "sid", tmp_result, "sid")
    query_result = project(tmp_result, ["address"])
    removeTable("Supply_tmp")
    removeTable(tmp_result)
    return query_result


def query_d():
    tmp_res1 = select(SUPPLIERS, "sname", "=", "Kiddie")
    tmp_res2 = select(SUPPLY, "pid", "=", "p20")
    tmp_result = join(tmp_res1, "sid", tmp_res2, "sid")
    query_result = project(tmp_result, ["cost"])
    removeTable("Suppliers_tmp")
    removeTable("Supply_tmp")
    removeTable(tmp_result)
    return query_result


def query_e():
    tmp_result = select(SUPPLY, "cost", ">=", 47.00)
    tmp_res1 = join(PRODUCTS, "pid", tmp_result, "pid")
    tmp_res2 = join(SUPPLIERS, "sid", tmp_res1, "sid")
    query_result = project(tmp_res2, ["sname", "pname", "cost"])
    removeTable("Supply_tmp")
    removeTable(tmp_res1)
    removeTable(tmp_res2)
    return query_result


if __name__ == "__main__":
    # res = query_x()
    with open(os.path.join(OUTPUT_PATH, QUERY_RESULT), "a+") as qr:
        qr.write("Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.\r\n")

    res = query_a()
    displayTable(res, QUERY_RESULT)
    removeTable(res)
    removeTree(SUPPLIERS, "sid")

    with open(os.path.join(OUTPUT_PATH, QUERY_RESULT), "a+") as qr:
        qr.write("Remove the B+_tree from Suppliers.sid, and repeat Question a.\r\n")

    res = query_b()
    displayTable(res, QUERY_RESULT)
    removeTable(res)

    with open(os.path.join(OUTPUT_PATH, QUERY_RESULT), "a+") as qr:
        qr.write("Find the address of the suppliers who supplied ‘p15’.\r\n")

    res = query_c()
    displayTable(res, QUERY_RESULT)
    removeTable(res)

    with open(os.path.join(OUTPUT_PATH, QUERY_RESULT), "a+") as qr:
        qr.write("What is the cost of ‘p20’ supplied by ‘Kiddie’?\r\n")

    res = query_d()
    displayTable(res, QUERY_RESULT)
    removeTable(res)

    with open(os.path.join(OUTPUT_PATH, QUERY_RESULT), "a+") as qr:
        qr.write("For each supplier who supplied products with a cost of 47 or higher, list his/her name, product name and the cost.\r\n")

    res = query_e()
    displayTable(res, QUERY_RESULT)
    removeTable(res)

