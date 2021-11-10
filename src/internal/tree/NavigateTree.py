from __future__ import annotations
from typing import TypedDict, Type
from dotenv import dotenv_values
from collections import defaultdict
from re import search

from .TreeNode import TreeNode
from .FileNode import FileNode
from .FolderNode import FolderNode
from .NodeType import NodeType

config = dotenv_values(".env.dev")

class MetaData(TypedDict):
    name: str
    id: str

class NavigateTree:
    def __init__(self):
        self.root = FolderNode('root')
        self.itemsCount = defaultdict(lambda: 0)

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
        folderName, id = metaData['name'], metaData['id']
        destinationNode.children[folderName] = FolderNode(f"{folderName}{config['NAME_ID_FLAG']}{id}")
        return True

    def insertMultipleFolderNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False
        for metaData in metaDataList:
            folderName, id = metaData['name'], metaData['id']
            destinationNode.children[folderName] = FolderNode(f"{folderName}{config['NAME_ID_FLAG']}{id}")
        return True

    def insertFileNode(self, path: list[str], metaData: MetaData) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False
        self.updateItemsCount(path, 1)
        fileName, id = metaData['name'], metaData['id']
        destinationNode.children[fileName] = FileNode(f"{fileName}{config['NAME_ID_FLAG']}{id}")
        return True

    def insertMultipleFileNodeInSameFolderNode(self, path: list[str], metaDataList: list[MetaData]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False
        self.updateItemsCount(path, len(metaDataList))
        for metaData in metaDataList:
            fileName, id = metaData['name'], metaData['id']
            destinationNode.children[fileName] = FileNode(f"{fileName}{config['NAME_ID_FLAG']}{id}")
        return True

    def deleteFileNode(self, path: list[str], deleteFileName: str) -> bool:
        return self.deleteNode(NodeType.ITEM, path, deleteFileName)

    def deleteMultipleFileNodeInSameFolderNode(self, path: list[str], deleteFileNameList: list[str]) -> bool:
        return self.deleteMultipleNodeInSameFolderNode(NodeType.ITEM, path, deleteFileNameList)

    def deleteFolderNode(self, path: list[str], deleteFolderName: str) -> bool:
        return self.deleteNode(NodeType.NON_ITEM, path, deleteFolderName)

    def deleteMultipleFolderNodeInSameFolderNode(self, path: list[str], deleteFolderNameList: list[str]) -> bool:
        return self.deleteNode(NodeType.NON_ITEM, path, deleteFolderNameList)

    def deleteNode(self, nodeType: NodeType, path: list[str], deleteName: str) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

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
        
    def deleteMultipleNodeInSameFolderNode(self,nodeType: NodeType, path: list[str], deleteNameList: list[str]) -> bool:
        destinationNode = self.traverse(path)
        if destinationNode is None or not isinstance(destinationNode, FolderNode):
            return False

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
