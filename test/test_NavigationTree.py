from src.internal.tree import *

t = NavigateTree()

t.insertFolderNode([], {'name': 'test', 'id': 'test_id1'})
t.insertFolderNode([], {'name': 'test_two', 'id': 'test_id2'})
t.insertFolderNode([], {'name': 'test_five', 'id': 'test_id3'})
t.insertFileNode(['test_five'], {'name': 'file_in five', 'id': 'test_five_file'})
t.insertFileNode(['test'], {'name': 'test2', 'id': 'test_id4'})
t.insertFolderNode(['test'], {'name': 'test2_folder', 'id': 'test_id5'})
t.insertFolderNode(['test', 'test2_folder'], {'name': 'testeststset', 'id':'uuidv3'})
t.insertFileNode(['test', 'test2_folder', 'testeststset'], {'name': 'testINnner', 'id':'inner'})
t.insertFileNode(['test', 'test2_folder', 'testeststset'], {'name': 'testINnner123123', 'id':'inner'})
tem = t.traverse(['test'])
# print(tem.children.keys())
tem = t.traverse(['test', 'test2_folder'])
# print(tem.children.keys())
# t.deleteFolderNode(['test', 'test2_folder'], 'testeststset')
# print(tem.children.keys())
printNavigateTreeByDepth(t)

print(treeToJSON(t.root))
print(childrenToJSON(t.root))
