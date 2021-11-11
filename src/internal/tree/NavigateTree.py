from __future__ import annotations
from typing import Type
from dotenv import dotenv_values
from collections import defaultdict
from re import search

from .TreeNode import TreeNode
from .FileNode import FileNode
from .FolderNode import FolderNode
from .NodeType import NodeType
from .meta import MetaData

config = dotenv_values(".env.dev")

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
    
    def searchChildren(self, path: list[str], pattern: str) -> dict[str, str] | None: 
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return None

        result = {}
        for key, value in destinationNode.children.items():
            if search(pattern, key) is not None:
                result[key] = value['data']
        
        return result

    
    def searchAllSubChildren(self, path: list[str], pattern: str) -> Type[TreeNode] | None: 
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return None
        pass

    def insertFolderNode(self, path: list[str], metaData: MetaData) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False
        folderName, type, id = metaData['name'], str(metaData['type']), metaData['id']
        destinationNode.children[type+folderName] = FolderNode(metaData)
        return True

    def insertMultipleFolderNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False
        for metaData in metaDataList:
            folderName, type, id = metaData['name'], str(metaData['type']), metaData['id']
            destinationNode.children[type+folderName] = FolderNode(metaData)
        return True

    def insertFileNode(self, path: list[str], metaData: MetaData) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        self.updateItemsCount(path, 1)

        fileName, type, id = metaData['name'], str(metaData['type']), metaData['id']
        destinationNode.children[type+fileName] = FileNode(metaData)
        return True

    def insertMultipleFileNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        self.updateItemsCount(path, len(metaDataList))

        for metaData in metaDataList:
            fileName, type, id = metaData['name'], str(metaData['type']), metaData['id']
            destinationNode.children[type+fileName] = FileNode(metaData)
        return True

    def deleteFileNode(self, path: list[str], deleteFileId: str) -> bool:
        return self.deleteNode(NodeType.ITEM, path, deleteFileId)

    def deleteMultipleFileNodeInSameFolderNode(self, path: list[str], deleteFileIdList: list[str]) -> bool:
        return self.deleteMultipleNodeInSameFolderNode(NodeType.ITEM, path, deleteFileIdList)

    def deleteFolderNode(self, path: list[str], deleteFolderId: str) -> bool:
        return self.deleteNode(NodeType.NON_ITEM, path, deleteFolderId)

    def deleteMultipleFolderNodeInSameFolderNode(self, path: list[str], deleteFolderIdList: list[str]) -> bool:
        return self.deleteNode(NodeType.NON_ITEM, path, deleteFolderIdList)

    def deleteNode(self, nodeType: NodeType, path: list[str], deleteId: str) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        for d in destinationNode.children.values():
            value = d.data

            if deleteId == value['id']:
                deleteName = value['type'] + value['name']

        if nodeType == NodeType.ITEM:
            self.updateItemsCount(path, -1)
        elif nodeType == NodeType.NON_ITEM:
            self.updateItemsCount(path, -self.itemsCount['/'.join(path + [deleteName])])
            self.deleteItemsCount(path + [deleteName])

        try:
            del destinationNode.children[deleteName]
            return True
        except KeyError:
            return False
        
    def deleteMultipleNodeInSameFolderNode(self,nodeType: NodeType, path: list[str], deleteIdList: list[str]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

        deleteNameList = []
        for d in destinationNode.children.values():
            value = d.data

            if value['id'] in deleteIdList:
                deleteNameList.append(value['type'] + value['name'])

        if nodeType == NodeType.ITEM:
            self.updateItemsCount(path, -len(deleteNameList))
        elif nodeType == NodeType.NON_ITEM:
            for deleteName in deleteNameList:
                self.updateItemsCount(path, -self.itemsCount['/'.join(path + [deleteName])])
                self.deleteItemsCount(path + [deleteName])

        try:
            for deleteName in deleteNameList:
                del destinationNode.children[deleteName]
            return True
        except KeyError:
            return False
