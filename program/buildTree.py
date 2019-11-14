import TreeNode as tn
import ast
import math
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


#print(suppliers_data[0])

#function to builttree, i.e insert data entry in keys_list one by one
root=tn.Node()
tn.insert(root,5,'page01',2)
tn.insert(root,6,'page02',2)
print(root.keys)
print(root.pointers)
print(tn.search(root,7)[1])
def buildTree(root,keys_list,order):
     # code to be completed
     pass



        
       




       
           




