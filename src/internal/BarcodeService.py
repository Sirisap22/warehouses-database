import os
import json

class BarcodeService:
    def __init__(self, name: str, repoPath: str) -> None:
        self.barcode = {}

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
        
        self.loadBarcode()
    
    def mapBarcode(self, barcode: str) -> dict[str, str]:
        return self.barcode[barcode[-4:]]


    def saveConfig(self) -> None:
        name = self.config["name"]
        p = f"_{name}.cnfg"
        with open(f"{self.config['path']}/{p}", "w") as f:
            f.write(json.dumps(self.config))

    def doConfig(self, param: str, val: str | int) -> None:
        self.config[param] = val
        self.saveConfig()

    def barcodePath(self) -> str:
        name = self.config["name"]
        path = self.config["path"]
        return f"{path}/{name}.txt"
    
    def loadBarcode(self) -> None:
        with open(self.barcodePath(), "r", encoding="utf-8") as f:
            for line in f.readlines():
                code, name, description, tag =  list(map(lambda x: x.strip("\""), line.rstrip("\n").split(":")))
                self.barcode[code] = {
                    "name": name,
                    "description": description,
                    "tag": tag
                }

