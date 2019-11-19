from program.relAlg import select, project, join
from program.display import displayTable
from program.remove import removeTree, removeTable

SUPPLY = "Supply"
PRODUCTS = "Products"
SUPPLIERS = "Suppliers"


def query_a():
    tmp_result = select(SUPPLIERS, "sid", "<=", "s23")
    query_result = project(tmp_result, ["sname"])
    return query_result


def query_b():
    tmp_result = select(SUPPLIERS, "sid", "=", "s23")
    query_result = project(tmp_result, ["sname"])
    return query_result


def query_c():
    tmp_result = select(SUPPLY, "pid", "=", "p15")
    tmp_result = join(SUPPLIERS, "sid", tmp_result, "sid")
    project(tmp_result, ["address"])


def query_d():
    tmp_result = select(SUPPLIERS, "sname", "=", "Kiddie")
    tmp_result = select(tmp_result, "pid", "=", "p20")
    tmp_result = join(tmp_result, "sid", SUPPLY, "sid")
    project(tmp_result, ["cost"])


def query_e():
    tmp_result = select(SUPPLY, "cost", ">=", 47.00)
    tmp_result = join(tmp_result, "pid", PRODUCTS, "pid")
    tmp_result = join(tmp_result, "sid", SUPPLIERS, "sid")
    project(tmp_result, ["sname", "pname", "cost"])


if __name__ == "__main__":
    res = query_a()
    displayTable(res, "XXX.txt")
    removeTable(res)
    removeTree(SUPPLIERS, "sid")
    # query_b()
    # removeTable()
    # query_c()
    # removeTable()
    # query_d()
    # removeTable()
    # query_e()
    # removeTable()

