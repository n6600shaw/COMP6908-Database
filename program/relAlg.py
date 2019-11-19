import json
import os
from enum import Enum

import pandas as pd


DATA_PATH = "../data/"
INDEX_PATH = "../index/"
INDEX_DIRECTORY = "directory.txt"
PAGE_LINK = "pageLink.txt"
SCHEMAS = "schemas.txt"
PAGE_POOL = "pagePool.txt"

TYPE_POS = 0
CONTENT_POS = 2
RELATION_POS = 0
ATTR_POS = 1
ROOT_POS = 2

CAPACITY = 2


class INTERNAL_NODE(Enum):
    NODE_TYPE = 0
    PARENTAL_POINTER = 1
    CONTENT = 2


class LEAF_NODE(Enum):
    NODE_TYPE = 0
    PARENTAL_POINTER = 1
    LEFT_POINTER = 2
    RIGHT_POINTER = 3
    CONTENT = 4


class INDEX_TYPE(Enum):
    CLUSTERED_INDEX = 0
    UNCLUSTERED_INDEX = 1


class DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1


clustered_index = [("Products", "pid"), ("Suppliers", "sid"), ("Supply", "sid")]
unclustered_index = [
    ("Products", "pname"), ("Products", "color"),
    ("Suppliers", "sname"), ("Suppliers", "address"),
    ("Supply", "pid"), ("Supply", "cost")
]


def get_tuples_by_ci(pointer_wrapper, rel, op):
    pointer = pointer_wrapper[0]
    filename, index = pointer[:-2], int(pointer[-1])

    with open(os.path.join(DATA_PATH, rel, PAGE_LINK)) as pl:
        content = pl.readlines()[0]
        pages = json.loads(content)
        for idx, val in enumerate(pages):
            if val == filename:
                cursor = idx
                break

        res = []
        if op in ('<', '<='):
            for idx, val in enumerate(pages):
                if idx == cursor:
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        if op == '<' and index == 1 or op == '<=':
                            res.append(data[0])

                        if op == '<=' and index == 1:
                            res.append(data[1])

                    break

                with open(os.path.join(DATA_PATH, rel, val)) as f:
                    content = f.readlines()[0]
                    data = json.loads(content)
                    res += data
        elif op in ('>', '>='):
            for idx, val in enumerate(pages[cursor:]):
                with open(os.path.join(DATA_PATH, rel, val)) as f:
                    content = f.readlines()[0]
                    data = json.loads(content)
                    if idx == cursor:
                        if op == '>=' and index == 0:
                            res.append(data[0])

                        if op == '>' and index == 0 or op == '>=':
                            res.append(data[1])
                    else:
                        res += data
        elif op == '=':
            res = get_single_tuple(filename, index, rel, res)
        else:
            raise Exception('Invalid op value!!!')

    return res


def get_single_tuple(filename, index, rel, res):
    with open(os.path.join(DATA_PATH, rel, filename)) as f:
        content = f.readlines()[0]
        data = json.loads(content)
        res.append(data[index])

    return res


def get_data_files(rel, node_content, res):
    for item in node_content:
        if isinstance(item, list):
            pointer = item[0]
            filename, index = pointer[:-2], int(pointer[-1])
            with open(os.path.join(DATA_PATH, rel, filename)) as f:
                content = f.readlines()[0]
                data = json.loads(content)
                res.append(data[index])

    return res


def search(pointer, rel, res, direction=DIRECTION.LEFT):
    with open(os.path.join(INDEX_PATH, pointer)) as f:
        node = f.readlines()[0]
        data = json.loads(node)
        content = data[LEAF_NODE.CONTENT.value]
        if direction == DIRECTION.LEFT:
            content.reverse()
        res = get_data_files(rel, content, res)
        next_pointer = data[LEAF_NODE.LEFT_POINTER.value if direction == DIRECTION.LEFT else LEAF_NODE.RIGHT_POINTER.value]

    if next_pointer != "nil":
        res = search(next_pointer, rel, res, direction)
    return res


def get_tuples_by_ui(leaf_node, rel, val, op):
    res = []
    content = leaf_node[LEAF_NODE.CONTENT.value]
    if op in ('<', '<='):
        content.reverse()
        for index, value in enumerate(content):
            if (isinstance(value, str) and value == val and op == '<=') or (isinstance(value, str) and value < val):
                pointer_wrapper = content[index - 1]
                pointer = pointer_wrapper[0]
                filename, index = pointer[:-2], int(pointer[-1])
                res = get_single_tuple(filename, index, rel, res)
        if leaf_node[LEAF_NODE.LEFT_POINTER.value] != "nil":
            res = search(leaf_node[LEAF_NODE.LEFT_POINTER.value], rel, res, DIRECTION.LEFT)
    elif op in ('>', '>='):
        for index, value in enumerate(content):
            if (isinstance(value, str) and value == val and op == '>=') or (isinstance(value, str) and value > val):
                pointer_wrapper = content[index + 1]
                pointer = pointer_wrapper[0]
                filename, index = pointer[:-2], int(pointer[-1])
                res = get_single_tuple(filename, index, rel, res)
        if leaf_node[LEAF_NODE.RIGHT_POINTER.value] != "nil":
            res = search(leaf_node[LEAF_NODE.RIGHT_POINTER.value], rel, res, DIRECTION.RIGHT)
    elif op == '=':
        for index, value in enumerate(content):
            if isinstance(value, str) and value == val:
                pointer_wrapper = content[index + 1]
                pointer = pointer_wrapper[0]
                filename, index = pointer[:-2], int(pointer[-1])
                res = get_single_tuple(filename, index, rel, res)
    else:
        raise Exception('Invalid op value!!!')

    return res


def dfs(filename, rel, val, op, index_type=INDEX_TYPE.CLUSTERED_INDEX):
    res = None
    with open(os.path.join(INDEX_PATH, filename)) as f:
        info = f.readlines()[0]
        data = json.loads(info)
        if data[TYPE_POS] == "I":
            content = data[CONTENT_POS]
            located = False
            for index, value in enumerate(content):
                if not value.endswith(".txt"):
                    if val < value:
                        res = dfs(content[index - 1], rel, val, op, index_type)
                        located = True
                        break
                    if val == value:
                        res = dfs(content[index + 1], rel, val, op, index_type)
                        located = True
                        break

            if not located:
                res = dfs(content[-1], rel, val, op, index_type)
        else:
            if index_type == INDEX_TYPE.CLUSTERED_INDEX:
                content = data[LEAF_NODE.CONTENT.value]
                for index, value in enumerate(content):
                    if isinstance(value, str) and value == val:
                        res = get_tuples_by_ci(content[index + 1], rel, op)
            else:
                res = get_tuples_by_ui(data, rel, val, op)

    return res


def get_page():
    # get page from page pool
    with open(os.path.join(DATA_PATH, PAGE_POOL)) as pp:
        content = pp.readlines()[0]
        page_pool = json.loads(content)
        if page_pool:
            page = page_pool.pop(0)
        else:
            raise Exception("Run out of pages!!!")

    # update page pool
    with open(os.path.join(DATA_PATH, PAGE_POOL), 'w') as f:
        f.write(json.dumps(page_pool))
    return page


def select(rel, att, op, val):
    res = None
    tree_root = None
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
        content = id_.readlines()[0]
        tuples = json.loads(content)
        for tuple_ in tuples:
            if tuple_[RELATION_POS] == rel and tuple_[ATTR_POS] == att:
                tree_root = tuple_[ROOT_POS]
                break

    schema = get_schema(rel)

    data = []
    if tree_root:
        index_type = INDEX_TYPE.UNCLUSTERED_INDEX
        for ci in clustered_index:
            if rel == ci[0] and att == ci[1]:
                index_type = INDEX_TYPE.CLUSTERED_INDEX
                break

        res = dfs(tree_root, rel, val, op, index_type)
        print("With B+_tree, the cost of searching {att} {op} {val} on {rel} is {value} pages".format(rel=rel,
                                                                                                      att=att,
                                                                                                      op=op,
                                                                                                      val=val,
                                                                                                      value="???"))
    else:
        with open(os.path.join(DATA_PATH, rel, PAGE_LINK)) as pl:
            content = pl.readlines()[0]
            pages = json.loads(content)
            for page in pages:
                with open(os.path.join(DATA_PATH, rel, page)) as pg:
                    page_content = pg.readlines()[0]
                    page_data = json.loads(page_content)
                    data += page_data

            df = pd.DataFrame(data, columns=schema)
            if op == '<':
                df = df.loc[df[att] < val]
            elif op == '<=':
                df = df.loc[df[att] <= val]
            elif op == '=':
                df = df.loc[df[att] == val]
            elif op == '>':
                df = df.loc[df[att] > val]
            elif op == '>=':
                df = df.loc[df[att] >= val]
            else:
                raise Exception('Invalid op value!!!')
            res = df.values.tolist()

        print("Without B+_tree, the cost of searching {att} {op} {val} on {rel} is {value} pages".format(rel=rel,
                                                                                                         att=att,
                                                                                                         op=op,
                                                                                                         val=val,
                                                                                                         value="???"))

    # TODO: print the total number of pages read from B+ tree or from data files
    write_to_pages(rel, res)

    return rel


def get_schema(rel):
    with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
        content = sc.readlines()[0]
        fields = json.loads(content)
        fields = [field for field in fields if field[0] == rel]
        fields.sort(key=lambda x: x[3])
        schema = [field[1] for field in fields]
    return schema


def write_to_pages(rel, res):
    rel_name = rel
    if os.path.exists(os.path.join(DATA_PATH, rel)):
        rel_name = rel + "_tmp"
        os.mkdir(os.path.join(DATA_PATH, rel_name))
    else:
        os.mkdir(os.path.join(DATA_PATH, rel))

    length = len(res)
    for i in range(0, length, CAPACITY):
        page = get_page()
        with open(os.path.join(DATA_PATH, rel_name, page), "w") as f:
            f.write(json.dumps(res[i:i + CAPACITY]))


def update_schemas(rel, attList):
    new_items = []
    for index, value in enumerate(attList):
        # TODO: get the correct type for each field
        new_items.append([rel, value, "str", index])
    with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
        content = sc.readlines()[0]
        schemas = json.loads(content)

    schemas += new_items
    with open(os.path.join(DATA_PATH, SCHEMAS), 'w') as f:
        f.write(json.dumps(schemas))


def project(rel, attList):
    tmp_path = os.path.join(DATA_PATH, rel + "_tmp")
    # TODO: handle the case when path is the initial folder
    path = tmp_path if os.path.exists(tmp_path) else os.path.join(DATA_PATH, rel)
    page_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        page_files = filenames

    data = []
    for page_file in page_files:
        with open(os.path.join(tmp_path, page_file)) as f:
            content = f.readlines()[0]
            two_tuples = json.loads(content)
            data += two_tuples

    schema = get_schema(rel)
    df = pd.DataFrame(data, columns=schema)
    df = df.filter(attList)
    df.drop_duplicates(keep=False, inplace=True)
    data = df.values.tolist()

    res = name_the_new_relation(attList, rel)
    update_schemas(res, attList)
    write_to_pages(res, data)

    return res


def name_the_new_relation(attList, rel):
    return rel[:3] + "_" + attList[0][:3]


def join(rel1, att1, rel2, att2):
    with open(rel1) as f1, open(rel2) as f2:
        content1 = f1.readlines()[0]
        content2 = f2.readlines()[0]
        data1 = json.loads(content1)
        data2 = json.loads(content2)
        df1 = pd.DataFrame(data1[1:], columns=data1[0])
        df2 = pd.DataFrame(data2[1:], columns=data2[0])
        df = pd.merge(df1, df2, left_on=att1, right_on=att2, how='inner')
        res = [df.columns.values.tolist()] + df.values.tolist()

    tmp_result = "../data/Temporary/tmp.txt"
    with open(tmp_result, "w") as f:
        f.write(json.dumps(res))

    return tmp_result
