import os
import pickle
import json

from .tree import NavigateTree, MetaData, NodeType


class TreeService:
    def __init__(self, name: str, repoPath: str) -> None:
        self.navigationTree = None

        def mkdir(path: str) -> None:
            fullPath = f"{path}"
            if os.path.exists(fullPath):
                return
            else:
                os.mkdir(fullPath)
        def isExist(path: str, name: str) -> bool:
            fullPath = f"{path}/{name}"
            return os.path.isfile(fullPath)
        
        configFileName = f"_{name}.cnfg"
        if isExist(repoPath, configFileName):
            self.config = json.loads(open(f"{repoPath}/{configFileName}", "r").read())
        else:
            mkdir(repoPath)
            self.config = {
                "name" : name,
                "path" : repoPath,
            } 
            self.saveConfig()

        objectFileName = f"{name}.pkl"
        if isExist(repoPath, objectFileName):
            self.loadObject()
        else:
            self.initializeObject()

    def saveConfig(self) -> None:
        name = self.config["name"]
        p = f"_{name}.cnfg"
        with open(f"{self.config['path']}/{p}", "w") as f:
            f.write(json.dumps(self.config))

    def doConfig(self, param: str, val: str | int) -> None:
        self.config[param] = val
        self.saveConfig()

    def objectPath(self) -> str:
        name = self.config["name"]
        path = self.config["path"]
        return f"{path}/{name}.pkl"
    
    def initializeObject(self) -> None:
        self.navigationTree = NavigateTree()
        self.saveObject()
    
    def loadObject(self) -> None:
        with open(self.objectPath(), "rb") as f:
            self.navigationTree = pickle.load(f)

    def saveObject(self) -> None:
        with open(self.objectPath(), "wb") as f:
            pickle.dump(self.navigationTree, f)

    def insert(self, type: NodeType, path: str, metaData: MetaData) -> bool:
        path = path.split("/")
        if type == NodeType.NON_ITEM:
            return self.navigationTree.insertFolderNode(path, metaData)
        elif type == NodeType.ITEM:
            return self.navigationTree.insertFileNode(path, metaData)

    def insertMultiple(self, type: NodeType, path: str, metaDataList: list[MetaData]) -> bool:
        path = path.split("/")
        if type == NodeType.NON_ITEM:
            return self.navigationTree.insertMultipleFolderNodeInSameFolderNode(path, metaDataList)
        elif type == NodeType.ITEM:
            return self.navigationTree.insertMultipleFileNodeInSameFolderNode(path, metaDataList)

    def delete(self, type: NodeType, path: str, deleteName: str) -> bool:
        path = path.split("/")
        if type == NodeType.NON_ITEM:
            return self.navigationTree.deleteFolderNode(path, deleteName)
        elif type == NodeType.ITEM:
            return self.navigationTree.deleteFileNode(path, deleteName)

    def deleteMultiple(self, type: NodeType, path: str, deleteNameList: list[str]):
        path = path.split("/")
        if type == NodeType.NON_ITEM:
            return self.navigationTree.deleteMultipleFolderNodeInSameFolderNode(path, deleteNameList)
        elif type == NodeType.ITEM:
            return self.navigationTree.deleteMultipleFileNodeInSameFolderNode(path, deleteNameList)
    
    def search(self, path: str, pattern: str):
        pass