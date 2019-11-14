class Node:
    
    def __init__(self):
       self.node_type = 'L'
       self.parent = None
       self.pointers=['nil','nil']
       self.node_page = None
       self.keys=[]

def search(node, key):
      while(node.node_type!='L'):
          length=len(node.keys)
          for i in range(length-1):
            if(i==0 and key<node.keys[i]):
              node=node.pointers[i]
            elif (i+1==length-1 and key>node.keys[i]):
              node=node.pointers[length]
            else:
              if(key>=node.keys[i] and key<node.keys[i+1]):
                node=node.pointers[i+1]
      length=len(node.keys)
      index=None
      for i in range(length-1):
        if(node.keys[i]==key):
           index=i
      return node,index


def insert(node, key, pointer,order):

    #initiate bound
    #low_bound=1
    high_bound=order
    if(node.parent!=None):
        low_bound=order
        high_bound=2*order

    appendKey(node,key,pointer)

    if(len(node.keys)>high_bound):
    #if exceed node capacity
       #split node
           #if node is root
           split_res=splitNode(node)
           if(node.parent==None):
             #create two new node
             root=Node()
             insert(root,split_res[1],split_res[0],order)
           #if node is not root
           else:
             insert(node.parent,split_res[1],split_res[0],order)

#append key and pointer
def appendKey(node,key,pointer):
    node.keys.append(key)
    node.keys.sort()
    index=node.keys.index(key)
    node.pointers.insert(index+1,pointer)

#split node, redistribute keys and pointers
def splitNode(node):
     right=Node()
     total_keys=node.keys
     total_pointers=node.pointers
     node.keys=total_keys[0:int(round(len(total_keys)/2))]
     node.pointers=total_pointers[0:int(round(len(total_pointers)/2))]
     #if leaf copy up
     if(node.node_type=='L'):
       right.keys=total_keys[int(round(len(total_keys)/2))+1:len(total_keys)]
       right.pointers=total_pointers[int(round(len(total_pointers)/2))+1:len(total_pointers)]
     
     #if interval move up
     else:
       #move up
       right.keys=total_keys[int(round(len(total_keys)/2))+2:len(total_keys)]
       right.pointers=total_pointers[int(round(len(total_pointers)/2))+2:len(total_pointers)]
    
     return right,total_keys[int(round(len(total_keys)/2))+1]







