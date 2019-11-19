import json
import os

DATA_PATH = "../data/"
INDEX_PATH = "../index/"
OUTPUT_PATH = "../queryOutput/"
TREE_PIC_PATH = "../treePic/"
PAGE_LINK = "pageLink.txt"

TYPE_POS = 0
CONTENT_POS = 2


def dfs(filename, indent_no, distfile):
    with open(os.path.join(INDEX_PATH, filename)) as f:
        content = f.readlines()[0]
        distfile.write(" " * indent_no + filename + ": " + content + "\r\n")
        data = json.loads(content)
        if data[TYPE_POS] == "I":
            for entry in data[CONTENT_POS]:
                if entry.endswith(".txt"):
                    dfs(entry, indent_no + 2, distfile)


def displayTree(fname="pg06.txt"):
    if not os.path.exists(TREE_PIC_PATH):
        os.mkdir(os.path.join(TREE_PIC_PATH))
    indent_no = 0
    with open(os.path.join(INDEX_PATH, fname)) as root, open(os.path.join(TREE_PIC_PATH, "Suppliers_sid.txt"), "w") as tree_pic:
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
    with open(os.path.join(OUTPUT_PATH, fname), "w") as qr:
        qr.write(json.dumps(data))


if __name__ == "__main__":
    displayTree("pg80.txt")
