import json

import TreeNode as tn
from program.types import INDEX_PATH


def buildTree(rel, att, od):
    tuple_list = tn.getAttList(rel, att)
    # create root node
    root = tn.Node(tn.getPage())
    root = tn.insert(root, tuple_list[0][0], tuple_list[0][1], od, root)
    for i in range(1, len(tuple_list)):
        key = tuple_list[i][0]
        pointer = tuple_list[i][1]
        root = tn.insert(tn.search(root, key)[0], key, pointer, od, root)

    root.__write__()

    with open(INDEX_PATH + 'directory.txt') as f:
        directory = json.loads(f.read())

    # update directory
    with open(INDEX_PATH + 'directory.txt', 'w') as f:
        tree = []
        tree.append(rel)
        tree.append(att)
        tree.append(root.node_page)
        directory.append(tree)
        f.write(json.dumps(directory))
    print(root.__print__())


if __name__ == '__main__':
    buildTree('Suppliers', 'sid', 2)
