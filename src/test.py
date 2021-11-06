from warehouses import NavigateTree

t = NavigateTree()

def printNavigateTree(t):
    print('root |> ')


t.insertFolderNode([], {'name': 'test', 'id': 'test_id'})
t.insertFolderNode([], {'name': 'test_two', 'id': 'test_id'})
t.insertFolderNode([], {'name': 'test_five', 'id': 'test_id'})
t.insertFileNode(['test'], {'name': 'test2', 'id': 'test_id2'})
t.insertFolderNode(['test'], {'name': 'test2_folder', 'id': 'test_id2'})
t.insertFileNode(['test', 'test2_folder'], {'name': 'testeststset', 'id':'uuidv3'})
tem = t.traverse(['test'])
print(tem.children.keys())
tem = t.traverse(['test', 'test2_folder'])
print(tem.children.keys())
t.deleteFileNode(['test', 'test2_folder'], 'testeststset')
print(tem.children.keys())
print(t)