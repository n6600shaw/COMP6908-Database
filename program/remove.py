import json
import os
import shutil

DATA_PATH = "../data/"
INDEX_PATH = "../index/"
INDEX_DIRECTORY = "directory.txt"
PAGE_POOL = "pagePool.txt"
SCHEMAS = "schemas.txt"

TYPE_POS = 0
CONTENT_POS = 2
RELATION_POS = 0
ATTR_POS = 1
ROOT_POS = 2


def dfs(filename):
    with open(os.path.join(INDEX_PATH, filename)) as f:
        content = f.readlines()[0]
        data = json.loads(content)
        if data[TYPE_POS] == "I":
            pages = []
            for entry in data[CONTENT_POS]:
                if entry.endswith(".txt"):
                    dfs(entry)
                    pages.append(entry)
                    os.remove(os.path.join(INDEX_PATH, entry))

            with open(os.path.join(INDEX_PATH, PAGE_POOL)) as df:
                page_pool = json.loads(df.readlines()[0])
                page_pool.extend(pages)
                page_pool.sort(reverse=True)
            with open(os.path.join(INDEX_PATH, PAGE_POOL), 'w') as df:
                df.write(json.dumps(page_pool))


def removeTree(rel, att):
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as f:
        content = f.readlines()[0]
        tuples = json.loads(content)

        for tuple_ in tuples:
            if tuple_[RELATION_POS] == rel and tuple_[ATTR_POS] == att:
                dfs(tuple_[ROOT_POS])
                os.remove(os.path.join(INDEX_PATH, tuple_[ROOT_POS]))

    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY), "w") as f:
        res = json.dumps([tuple_ for tuple_ in tuples if tuple_[RELATION_POS] != rel or tuple_[ATTR_POS] != att])
        f.write(res)


def removeTable(rel):
    path = os.path.join(DATA_PATH, rel)
    if os.path.exists(path):
        page_files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            page_files = filenames

        with open(os.path.join(DATA_PATH, PAGE_POOL)) as pp:
            content = pp.readlines()[0]
            page_pool = json.loads(content)

        with open(os.path.join(DATA_PATH, PAGE_POOL), "w") as pp:
            res = json.dumps(page_pool + page_files)
            pp.write(res)

        with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
            content = sc.readlines()[0]
            fields = json.loads(content)

        fields = [field for field in fields if field[RELATION_POS] != rel]
        with open(os.path.join(DATA_PATH, SCHEMAS), "w") as sc:
            res = json.dumps(fields)
            sc.write(res)

        shutil.rmtree(path)
        with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
            indices = json.loads(id_.readlines()[0])
            for index in indices:
                if index[RELATION_POS] == rel:
                    removeTree(index[RELATION_POS], index[ATTR_POS])  # NOTICE: might be a bug here


if __name__ == "__main__":
    removeTable("Supply_tmp")
