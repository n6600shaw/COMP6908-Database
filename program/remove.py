import json
import os

INDEX_PATH = "../index/"
INDEX_DIRECTORY = "directory.txt"

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
            for entry in data[CONTENT_POS]:
                if entry.endswith(".txt"):
                    dfs(entry)
                    os.remove(os.path.join(INDEX_PATH, entry))
                    # TODO: release the occupied pages to the page pool


def removeTree(rel, att):
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as f:
        content = f.readlines()[0]
        tuples = json.loads(content)
        for tuple_ in tuples:
            if tuple_[RELATION_POS] == rel and tuple_[ATTR_POS] == att:
                dfs(tuple_[ROOT_POS])

    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY), "w") as f:
        res = json.dumps([tuple_ for tuple_ in tuples if tuple_[RELATION_POS] != rel or tuple_[ATTR_POS] != att])
        f.write(res)


def removeTable(rel):
    pass


if __name__ == "__main__":
    removeTree("Suppliers", "sid")
