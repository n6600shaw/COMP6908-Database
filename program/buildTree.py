import TreeNode as tn
import ast
import math

'''
path='../Data/Suppliers/'

f=open(path+"pageLink.txt")
pageLink=ast.literal_eval(f.read())
f.close()
#print(pageLink)

suppliers_data=[]
for page in pageLink:
   f=open(path+page)
   pageData=ast.literal_eval(f.read())
   f.close()
   suppliers_data+=pageData
'''

#print(suppliers_data[0])

#function to builttree, i.e insert data entry in keys_list one by one
root=tn.Node(tn.getPage())

tn.insert(root,5,'page01',2,root)
tn.insert(root,6,'page02',2,root)
#print(tn.search(root,6)[0])
root=tn.insert(tn.search(root,6)[0],7,'page03',2,root)
root=tn.insert(tn.search(root,10)[0],10,'page04',2,root)
root=tn.insert(tn.search(root,13)[0],13,'page05',2,root)
root=tn.insert(tn.search(root,12)[0],12,'page06',2,root)
root=tn.insert(tn.search(root,15)[0],15,'page06',2,root)
root=tn.insert(tn.search(root,16)[0],16,'page07',2,root)
root=tn.insert(tn.search(root,17)[0],17,'page07',2,root)
root=tn.insert(tn.search(root,18)[0],18,'page07',2,root)


print(root.__print__())
def buildTree(root,keys_list,order):
     # co
     # de to be completed
     pass




        
       





       
           




