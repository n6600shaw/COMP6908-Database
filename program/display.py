import json
import os

DATA_PATH = "../data/"
INDEX_PATH = "../index/"
OUTPUT_PATH = "../queryOutput/"
TREE_PIC_PATH = "../treePic/"
PAGE_LINK = "pageLink.txt"
INDEX_DIRECTORY = "directory.txt"

TYPE_POS = 0
CONTENT_POS = 2

RELATION_POS = 0
ATTR_POS = 1
ROOT_POS = 2


def dfs(filename, indent_no, distfile):
    with open(os.path.join(INDEX_PATH, filename)) as f:
        content = f.readlines()[0]
        distfile.write(" " * indent_no + filename + ": " + content + "\r\n")
        data = json.loads(content)
        if data[TYPE_POS] == "I":
            for entry in data[CONTENT_POS]:
                if entry.endswith(".txt"):
                    dfs(entry, indent_no + 2, distfile)


def get_rel_and_att(fname):
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
        content = id_.readlines()[0]
        tuples = json.loads(content)
        for tuple_ in tuples:
            if tuple_[ROOT_POS] == fname:
                rel = tuple_[RELATION_POS]
                att = tuple_[ATTR_POS]
                break
    return att, rel


def get_tree_pic_name(rel, att):
    return rel + "_" + att + ".txt"


def displayTree(fname="pg06.txt"):
    if not os.path.exists(TREE_PIC_PATH):
        os.mkdir(os.path.join(TREE_PIC_PATH))
    att, rel = get_rel_and_att(fname)
    tree_pic_name = get_tree_pic_name(rel, att)
    indent_no = 0
    with open(os.path.join(INDEX_PATH, fname)) as root, open(os.path.join(TREE_PIC_PATH, tree_pic_name), "w") as tree_pic:
        content = root.readlines()[0]
        tree_pic.write(" " * indent_no + fname + ": " + content + "\r\n")
        data = json.loads(content)
        if data[TYPE_POS] == "I":
            for entry in data[CONTENT_POS]:
                if entry.endswith(".txt"):
                    dfs(entry, indent_no + 2, tree_pic)


def displayTable(rel, fname):
    path = os.path.join(DATA_PATH, rel)
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files = filenames

    page_files = [file for file in files if file != PAGE_LINK]
    data = []
    for page_file in page_files:
        with open(os.path.join(path, page_file)) as f:
            content = f.readlines()[0]
            two_tuples = json.loads(content)
            data += two_tuples

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(os.path.join(OUTPUT_PATH))
    with open(os.path.join(OUTPUT_PATH, fname), "a+") as qr:
        qr.write(json.dumps(data) + "\r\n\r\n")


if __name__ == "__main__":
    displayTree("pg80.txt")
