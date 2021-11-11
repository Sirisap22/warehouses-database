from src.internal.tree import *
from src.internal.tree import MetaType

t = NavigateTree()

t.insertFolderNode([''], {'name': '1', 'id': 'testid1', 'type': MetaType.WAREHOUSE})
t.insertFolderNode([''], {'name': '2', 'id': 'testid2', 'type': MetaType.WAREHOUSE})
t.insertFolderNode([''], {'name': '3', 'id': 'testid3', 'type': MetaType.WAREHOUSE})
t.insertFolderNode(['warehouse3'], {'name': 'A', 'id': 'testfivefile', 'type': MetaType.ZONE})
t.insertFolderNode(['warehouse1'], {'name': 'A', 'id': 'testid5', 'type': MetaType.ZONE})
t.insertFolderNode(['warehouse1'], {'name': 'B', 'id': 'testid4', 'type': MetaType.ZONE})
t.insertFolderNode(['warehouse1', 'zoneA'], {'name': '1', 'id':'uuidv3', 'type': MetaType.SHELF})
t.insertFileNode(['warehouse1', 'zoneA', 'shelf1'], {'name': 'testINnnasfdasfer', 'id':'asdf', 'type': MetaType.ITEM})
t.insertFileNode(['warehouse1', 'zoneA', 'shelf1'], {'name': 'testINnnasfdaasfsfer1111', 'id':'inner', 'type': MetaType.ITEM} )
t.insertFolderNode(['warehouse3', 'zoneA'], {'name': '1', 'id':'inner', 'type': MetaType.SHELF})
t.insertFileNode(['warehouse3', 'zoneA', 'shelf1'], {'name': 'testINnner123123', 'id':'inner', 'type': MetaType.ITEM})
tem = t.traverse(['warehouse1'])
# print(tem.children.keys())
tem = t.traverse(['warehouse1', 'zoneA'])
# print(tem.children.keys())
# t.deleteFolderNode(['warehouse1', 'zoneA'], 'shelf1')
# print(tem.children.keys()
printNavigateTreeByDepth(t)

print(treeToJSON(t.root))
print('count' ,t.itemsCount)

# d = breathFirstSearchLimit(t.root, 2)
arr = []
# print(breathFirstSearchLimit(t.root, 2))
# print(childrenToJSON(t.root))

def getWarehouses():
    warehouses = []
    for i, (warehouseKey, warehouseValue) in enumerate(t.root.children.items()):
        wD = warehouseValue.data
        wType, wName, wId = str(wD['type']), wD['name'], wD['id']
        warehouses.append({
            'warehouse' : wName,
            'zone': []
        })
        for zoneKey, zoneValue in t.root.children[warehouseKey].children.items():
            zD = zoneValue.data
            zType, zName, zId = str(zD['type']), zD['name'], zD['id']
            warehouses[i]['zone'].append({
                'name': zName,
                'item': t.itemsCount[f'{wType+wName}/{zType+zName}']
            })


    return warehouses

def getZone(path: str):
    destinationNode = t.traverse(path.split('/'))
    zone = []
    if destinationNode is not None:
        for key, value in destinationNode.children.items():
            sD = value.data
            type, name, id = str(sD['type']), sD['name'], sD['id']
            zone.append({
                'shelf': name,
                'item': t.itemsCount[path+f'/{type+name}']
            })
    return zone

def getItems(path):
    destinationNode = t.traverse(path.split('/'))
    items = []
    if destinationNode is not None:
        for key, value in destinationNode.children.items():
            iD = value.data
            type, name, id = str(iD['type']), iD['name'], iD['id']
            items.append({
                'item': name,
                'id': id
            })
    return items



print(getWarehouses())
print(getZone('warehouse1/zoneA'))
print(getItems('warehouse1/zoneA/shelf1'))

