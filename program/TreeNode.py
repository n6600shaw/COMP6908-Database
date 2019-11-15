class Node:
    
    def __init__(self,page):
       self.node_type = 'L'
       self.parent = None
       self.pointers=[]
       self.node_page = page
       self.keys=[]

    def __print__(self, level=0):
        ret = "\t"*level+repr(self.keys)+"\n"
        if(self.node_type!='L'):
            for pointer in self.pointers:
               ret += pointer.__print__(level+1)
        return ret


def search(node, key):
      while(node.node_type!='L'):
          length=len(node.keys)
          if(key<node.keys[0]):
              node=node.pointers[0]
          elif(key>=node.keys[length-1]):
              node=node.pointers[length]
          else:
             for i in range(length-1):
               if(key>=node.keys[i] and key<node.keys[i+1]):
                   node=node.pointers[i+1]
      length=len(node.keys)
      index=None
      for i in range(length):
        if(node.keys[i]==key):
           index=i
      return node,index
      


def insert(node, key, pointer,order,root):

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
             #create a new root
             root=Node(getPage())
             print("new root")
             root.node_type='I'
             #assign the new root as the parent of the new split nodes
             node.parent=root             
             split_res[0].parent=root
             #append node to new root's pointers
             root.pointers.append(node)
             insert(root,split_res[1],split_res[0],order,root)
           #if node is not root
           else:
             #assign node's parent as the new split node's parent
             split_res[0].parent=node.parent
             root=insert(node.parent,split_res[1],split_res[0],order,root)
    
    return root

#append key and pointer
def appendKey(node,key,pointer):
    node.keys.append(key)
    node.keys.sort()
    index=node.keys.index(key)
    if(node.node_type!='L'):
       index+=1
    node.pointers.insert(index,pointer)

#split node, redistribute keys and pointers
def splitNode(node):
     
     right=Node(getPage())
     right.node_type=node.node_type
     total_keys=node.keys
     total_pointers=node.pointers
     node.keys=total_keys[0:int(round(len(total_keys)/2))]
     node.pointers=total_pointers[0:int(round(len(total_pointers)/2))]
     #if leaf copy up
     if(node.node_type=='L'):
       right.keys=total_keys[int(round(len(total_keys)/2)):len(total_keys)]
       right.pointers=total_pointers[int(round(len(total_pointers)/2)):len(total_pointers)]
     #if interval move up
     else:
       #move up
       right.keys=total_keys[int(round(len(total_keys)/2))+1:len(total_keys)]
       right.pointers=total_pointers[int(round(len(total_pointers)/2)):len(total_pointers)]
     #update child nodes's pare
     if(node.node_type!='L'):
        for i in range(len(right.pointers)):
            right.pointers[i].parent=right
     return right,total_keys[int(round(len(total_keys)/2))]


def getPage():
    pass

def getRecord():
    pass







