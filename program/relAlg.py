import json
import os
from enum import Enum

import pandas as pd


DATA_PATH = "../data/"
INDEX_PATH = "../index/"
INDEX_DIRECTORY = "directory.txt"
PAGE_LINK = "pageLink.txt"
SCHEMAS = "schemas.txt"

TYPE_POS = 0
CONTENT_POS = 2
RELATION_POS = 0
ATTR_POS = 1
ROOT_POS = 2


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


def search(pointer, rel, att, res, direction=DIRECTION.LEFT):
    with open(os.path.join(INDEX_PATH, pointer)) as f:
        node = f.readlines()[0]
        data = json.loads(node)
        content = data[LEAF_NODE.CONTENT.value]
        if direction == DIRECTION.LEFT:
            content.reverse()
        res = get_data_files(rel, content, res)
        next_pointer = data[LEAF_NODE.LEFT_POINTER.value if direction == DIRECTION.LEFT else LEAF_NODE.RIGHT_POINTER.value]

    if next_pointer != "nil":
        res = search(next_pointer, rel, att, res, direction)
    return res


def get_tuples_by_ui(leaf_node, rel, att, val, op):
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
            res = search(leaf_node[LEAF_NODE.LEFT_POINTER.value], rel, att, res, DIRECTION.LEFT)
    elif op in ('>', '>='):
        for index, value in enumerate(content):
            if (isinstance(value, str) and value == val and op == '>=') or (isinstance(value, str) and value > val):
                pointer_wrapper = content[index + 1]
                pointer = pointer_wrapper[0]
                filename, index = pointer[:-2], int(pointer[-1])
                res = get_single_tuple(filename, index, rel, res)
        if leaf_node[LEAF_NODE.RIGHT_POINTER.value] != "nil":
            res = search(leaf_node[LEAF_NODE.RIGHT_POINTER.value], rel, att, res, DIRECTION.RIGHT)
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


def dfs(filename, rel, att, val, op, index_type=INDEX_TYPE.CLUSTERED_INDEX):
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
                        res = dfs(content[index - 1], rel, att, val, op, index_type)
                        located = True
                        break
                    if val == value:
                        res = dfs(content[index + 1], rel, att, val, op, index_type)
                        located = True
                        break

            if not located:
                res = dfs(content[-1], rel, att, val, op, index_type)
        else:
            if index_type == INDEX_TYPE.CLUSTERED_INDEX:
                content = data[LEAF_NODE.CONTENT.value]
                for index, value in enumerate(content):
                    if isinstance(value, str) and value == val:
                        res = get_tuples_by_ci(content[index + 1], rel, op)
            else:
                res = get_tuples_by_ui(data, rel, att, val, op)

    return res


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

    with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
        content = sc.readlines()[0]
        fields = json.loads(content)
        fields = [field for field in fields if field[0] == rel]
        fields.sort(key=lambda x: x[3])
        schema = [field[1] for field in fields]

    data = []
    if tree_root:
        index_type = INDEX_TYPE.UNCLUSTERED_INDEX
        for ci in clustered_index:
            if rel == ci[0] and att == ci[1]:
                index_type = INDEX_TYPE.CLUSTERED_INDEX
                break

        res = dfs(tree_root, rel, att, val, op, index_type)
        res = [schema] + res
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
            res = [df.columns.values.tolist()] + df.values.tolist()

    # TODO: print the total number of pages read from B+ tree or from data files
    tmp_result = "../data/Temporary/tmp.txt"
    with open(tmp_result, "w") as f:
        f.write(json.dumps(res))

    return tmp_result


def project(rel, attList):
    with open(rel) as f:
        content = f.readlines()[0]
        data = json.loads(content)
        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.filter(attList)
        df.drop_duplicates(keep=False, inplace=True)
        res = [df.columns.values.tolist()] + df.values.tolist()

    tmp_result = "../data/Temporary/tmp.txt"
    with open(tmp_result, "w") as f:
        f.write(json.dumps(res))

    return tmp_result


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
