from relAlg import select, project, join

SUPPLY = "Supply"
PRODUCTS = "Products"
SUPPLIERS = "Suppliers"


def query_a():
    tmp_result = select(SUPPLIERS, "sid", "=", "s23")
    query_result = project(tmp_result, ["sname"])
    print(query_result)


def query_b():
    tmp_result = select(SUPPLIERS, "sid", "=", "s23")
    query_result = project(tmp_result, ["sname"])
    print(query_result)


def query_c():
    tmp_result = select(SUPPLY, "pid", "=", "p15")
    tmp_result = join(SUPPLIERS, "sid", tmp_result, "sid")
    project(tmp_result, ["address"])


def query_d():
    tmp_result = select(SUPPLIERS, "sname", "=", "Kiddie")
    tmp_result = join(tmp_result, "sid", SUPPLY, "sid")
    tmp_result = select(tmp_result, "pid", "=", "p20")
    project(tmp_result, ["cost"])


def query_e():
    tmp_result = select(SUPPLY, "cost", ">=", 47.00)
    tmp_result = join(tmp_result, "pid", PRODUCTS, "pid")
    tmp_result = join(tmp_result, "sid", SUPPLIERS, "sid")
    project(tmp_result, ["sname", "pname", "cost"])


if __name__ == "__main__":
    # query_a()
    # query_b()
    query_c()
    # query_d()
    # query_e()

