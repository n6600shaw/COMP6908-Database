import json
import os

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

CLUSTERED_INDEX = [("Products", "pid"), ("Suppliers", "sid"), ("Supply", "sid")]
UNCLUSTERED_INDEX = [
    ("Products", "pname"), ("Products", "color"),
    ("Suppliers", "sname"), ("Suppliers", "address"),
    ("Supply", "pid"), ("Supply", "cost")
]


def get_tuples(pointer_wrapper, rel, op):
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
            with open(os.path.join(DATA_PATH, rel, filename)) as f:
                content = f.readlines()[0]
                data = json.loads(content)
                res.append(data[index])
        else:
            raise Exception('Invalid op value!!!')

    return res


def dfs(filename, rel, val, op):
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
                        res = dfs(content[index - 1], rel, val, op)
                        located = True
                        break
                    if val == value:
                        res = dfs(content[index + 1], rel,  val, op)
                        located = True
                        break

            if not located:
                res = dfs(content[-1], rel,  val, op)
        else:
            content = data[-1]
            for index, value in enumerate(content):
                if isinstance(value, str) and value == val:
                    res = get_tuples(content[index + 1], rel, op)
                else:
                    pass
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
        res = dfs(tree_root, rel, val, op)
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
