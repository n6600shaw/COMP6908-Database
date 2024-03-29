import json
import math

from program.types import DATA_PATH, INDEX_PATH, PAGE_LINK, SCHEMAS, PAGE_POOL


class Node:

    def __init__(self, page):
        self.node_type = 'L'
        self.parent = None
        self.pointers = []
        self.node_page = page
        self.keys = []
        self.left = None
        self.right = None
        self.info = []

    def __write__(self):
        node_data = []
        if self.node_type == 'I':
            for i in range(len(self.keys)):
                node_data.append(self.pointers[i].node_page)
                node_data.append(self.keys[i])
            node_data.append(self.pointers[len(self.pointers) - 1].node_page)
            self.info.append(self.node_type)
            if self.parent is not None:
                self.info.append(self.parent.node_page)
            else:
                self.info.append('nil')
            self.info.append(node_data)
        else:
            for i in range(len(self.keys)):
                node_data.append(self.keys[i])
                node_data.append(self.pointers[i])
            self.info.append(self.node_type)
            self.info.append(self.parent.node_page)
            if self.left is not None:
                self.info.append(self.left.node_page)
            else:
                self.info.append('nil')
            if self.right is not None:
                self.info.append(self.right.node_page)
            else:
                self.info.append('nil')
            self.info.append(node_data)

        # write node info to page

        with open(INDEX_PATH + self.node_page, 'w') as f:
            f.write(json.dumps(self.info))


        # go to children nodes
        if self.node_type != 'L':
            for pointer in self.pointers:
                pointer.__write__()

    # write tree data into files and print the tree structure
    def __print__(self, level=0):

        # ret = "\t" * level + repr(self.node_page + ":" + str(self.info)) + "\n"
        ret = "\t" * level + repr(self.keys) + repr(self.pointers) + "\n"
        if self.node_type != 'L':
            for pointer in self.pointers:
                ret += pointer.__print__(level + 1)
        return ret


def search(node, key):
    while node.node_type != 'L':
        length = len(node.keys)

        if key < node.keys[0]:
            node = node.pointers[0]
        elif key >= node.keys[length - 1]:
            node = node.pointers[length]
        else:
            for i in range(length - 1):
                if node.keys[i] <= key < node.keys[i + 1]:
                    node = node.pointers[i + 1]
                    break
    length = len(node.keys)
    index = None
    for i in range(length):
        if node.keys[i] == key:
            index = i
    return node, index


def insert(node, key, pointer, order, root):
    # initiate bound
    # low_bound=1
    high_bound = order
    if node.parent is not None:
        low_bound = order
        high_bound = 2 * order

    appendKey(node, key, pointer)

    if len(node.keys) > high_bound:
        # if exceed node capacity
        # split node
        # if node is root
        split_res = splitNode(node)
        if node.parent is None:
            # create a new root
            root = Node(getPage())
            print("new root")
            root.node_type = 'I'
            # assign the new root as the parent of the new split nodes
            node.parent = root
            split_res[0].parent = root
            # append node to new root's pointers
            root.pointers.append(node)
            insert(root, split_res[1], split_res[0], order, root)
        # if node is not root
        else:
            # assign node's parent as the new split node's parent
            split_res[0].parent = node.parent
            root = insert(node.parent, split_res[1], split_res[0], order, root)

    return root


# append key and pointer
def appendKey(node, key, pointer):
    check = False
    if key not in node.keys:
        check = True
        node.keys.append(key)
        node.keys.sort()
    index = node.keys.index(key)
    if node.node_type != 'L':
        index += 1
        node.pointers.insert(index, pointer)
    else:
        if check:
            node.pointers.insert(index, [pointer])
        else:
            node.pointers[index].append(pointer)



# split node, redistribute keys and pointers
def splitNode(node):
    right = Node(getPage())
    right.node_type = node.node_type
    total_keys = node.keys
    total_pointers = node.pointers
    node.keys = total_keys[0:int(math.floor(len(total_keys) / 2))]
    node.pointers = total_pointers[0:int(math.floor(len(total_pointers) / 2))]
    # if leaf copy up
    if node.node_type == 'L':
        right.keys = total_keys[int(math.floor(len(total_keys) / 2)):len(total_keys)]
        right.pointers = total_pointers[int(math.floor(len(total_pointers) / 2)):len(total_pointers)]
        # assign left and right
        node.right = right
        right.left = node
    # if interval move up
    else:
        # move up
        right.keys = total_keys[int(math.floor(len(total_keys) / 2)) + 1:len(total_keys)]
        right.pointers = total_pointers[int(math.floor(len(total_pointers) / 2)):len(total_pointers)]
    # update child nodes's pare
    if node.node_type != 'L':
        for i in range(len(right.pointers)):
            right.pointers[i].parent = right
    return right, total_keys[int(math.floor(len(total_keys) / 2))]


def getPage():
    path = INDEX_PATH + PAGE_POOL

    # get page from page pool
    with open(path) as f:
        page_pool = json.loads(f.read())
        if page_pool:
            page = page_pool.pop(0)

    # update page pool
    with open(path, 'w') as f:
        res = json.dumps(page_pool)
        f.write(res)
    return page


def getAttList(rel, att):
    # get attribute index in table
    with open(DATA_PATH + SCHEMAS) as f:
        content = f.readlines()[0]
        schemas = json.loads(content)
    for schema in schemas:
        if schema[0] == rel and schema[1] == att:
            att_index = schema[3]

    # get attribute list
    res = []
    with open(DATA_PATH + rel + '/' + PAGE_LINK) as f:
        content = f.readlines()[0]
        page_link = json.loads(content)
        for page in page_link:
            with open(DATA_PATH + rel + '/' + page) as pf:
                page_content = pf.readlines()[0]
                records = json.loads(page_content)
                for record in records:
                    res.append((record[att_index], page + '.' + str(records.index(record))))
    return res

