from __future__ import annotations
from typing import Type
from dotenv import dotenv_values
from collections import defaultdict
from re import search

from .TreeNode import TreeNode
from .FileNode import FileNode
from .FolderNode import FolderNode
from .NodeType import NodeType
from ..linked_structures import Queue
from .meta import MetaData

config = dotenv_values(".env")

def defaultVal():
    return 0

class NavigateTree:
    def __init__(self):
        self.root = FolderNode('root')
        self.itemsCount = defaultdict(defaultVal)

    def jsonable(self):
        return self.__dict__

    def updateItemsCount(self, path: list[str], count: int) -> None:
            curPath = ''
            self.itemsCount['root'] += count
            for step in path:
                if curPath == '':
                    curPath = '/'.join([step])
                else:
                    curPath = '/'.join([curPath, step])
                self.itemsCount[curPath] += count


    def deleteItemsCount(self, path: list[str]) -> None:
        path = '/'.join(path)
        toDeleteKeys = []
        for key in self.itemsCount.keys():
            if key.startswith(path):
               toDeleteKeys.append(key)

        for key in toDeleteKeys:
            del self.itemsCount[key]
    
    def traverse(self, path: list[str]) -> Type[TreeNode] | None:
        if path[0] == '':
            return self.root

        try:
            destinationNode = self.root
            for step in path:
               destinationNode = destinationNode.children[step] 
            return destinationNode
        except:
            return None
    
    def searchAllFileNode(self, path: list[str], pattern: str) -> list[str] | None: 
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return None
        
        searchedItemList = []
        queue = Queue([destinationNode])
        while not queue.isEmpty():
            curNode = queue.dequeue()

            if isinstance(curNode, FileNode):
                if search(pattern, curNode.data['name']) is not None: 
                    print(search(pattern, curNode.data['name']))
                    searchedItemList.append(curNode.data)
            
            else:
                for key, value in curNode.children.items():
                    queue.enqueue(value)

        return searchedItemList

    def insertFolderNode(self, path: list[str], metaData: MetaData) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        folderName, type, id = metaData['name'], str(metaData['type']), metaData['id']
        if type+folderName not in destinationNode.children:
            destinationNode.children[type+folderName] = FolderNode(metaData)
            return True

        return False

    def insertMultipleFolderNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        for metaData in metaDataList:
            folderName, type, id = metaData['name'], str(metaData['type']), metaData['id']
            if type+folderName in destinationNode.children:
                return False
            destinationNode.children[type+folderName] = FolderNode(metaData)

        return True

    def insertFileNode(self, path: list[str], metaData: MetaData) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        self.updateItemsCount(path, 1)

        fileName, type, id = metaData['name'], str(metaData['type']), metaData['id']
        if id not in destinationNode.children.keys():
            destinationNode.children[id] = FileNode(metaData)
            return True
        
        return False

    def insertMultipleFileNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        self.updateItemsCount(path, len(metaDataList))

        for metaData in metaDataList: 
            fileName, type, id = metaData['name'], str(metaData['type']), metaData['id']
            if id in destinationNode.children.keys():
                return False

        for metaData in metaDataList:
            fileName, type, id = metaData['name'], str(metaData['type']), metaData['id']
            destinationNode.children[id] = FileNode(metaData)
        return True

    def deleteFileNode(self, path: list[str], deleteFileId: str) -> bool:
        return self.deleteNode(NodeType.ITEM, path, deleteFileId)

    def deleteMultipleFileNodeInSameFolderNode(self, path: list[str], deleteFileIdList: list[str]) -> bool:
        return self.deleteMultipleNodeInSameFolderNode(NodeType.ITEM, path, deleteFileIdList)

    def deleteFolderNode(self, path: list[str], deleteFolderId: str) -> bool:
        return self.deleteNode(NodeType.NON_ITEM, path, deleteFolderId)

    def deleteMultipleFolderNodeInSameFolderNode(self, path: list[str], deleteFolderIdList: list[str]) -> tuple[bool, int, str]:
        return self.deleteMultipleNodeInSameFolderNode(NodeType.NON_ITEM, path, deleteFolderIdList)

    def deleteNode(self, nodeType: NodeType, path: list[str], deleteId: str) -> tuple[bool, int, str]:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return (False, 404, 'invalid path')

        for d in destinationNode.children.values():
            value = d.data

            if deleteId == value['id']:
                deleteName = value['type'] + value['name']

        try:
            if nodeType == NodeType.ITEM:
                self.updateItemsCount(path, -1)
                del destinationNode.children[deleteId]

            elif nodeType == NodeType.NON_ITEM:
                self.updateItemsCount(path, -self.itemsCount['/'.join(path + [deleteName])])
                self.deleteItemsCount(path + [deleteName])
                del destinationNode.children[deleteName]

                return (True, 200, 'successful')
        except KeyError:
            return (False, 404, 'key error')
        except UnboundLocalError:
            return (False, 404, 'id(s) not found')
        
    def deleteMultipleNodeInSameFolderNode(self,nodeType: NodeType, path: list[str], deleteIdList: list[str]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return (False, 404, 'invalid path')

        deleteNameList = []
        for d in destinationNode.children.values():
            value = d.data

            if value['id'] in deleteIdList:
                deleteNameList.append(str(value['type']) + value['name'])
        
        if len(deleteNameList) == 0:
            return (False, 404, 'id(s) not found')

        try:
            if nodeType == NodeType.ITEM:
                
                for deleteId in deleteIdList:
                    del destinationNode.children[deleteId]

                self.updateItemsCount(path, -len(deleteNameList))
                return (True, 200, 'successful')
            elif nodeType == NodeType.NON_ITEM:
                for deleteName in deleteNameList:
                    if self.itemsCount["/".join(path) + f"/{deleteName}"] > 0:
                        return (False, 403 , 'cannot delete folder(s) with item(s) in it')

                for deleteName in deleteNameList:
                    self.updateItemsCount(path, -self.itemsCount['/'.join(path + [deleteName])])
                    self.deleteItemsCount(path + [deleteName])

                for deleteName in deleteNameList:
                    del destinationNode.children[deleteName]
                return (True, 200, 'successful')
        except KeyError:
            return (False, 404, 'key error')
        except UnboundLocalError():
            return (False, 404, 'id(s) not found (unbound local error)')