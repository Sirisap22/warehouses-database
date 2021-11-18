import json
import os
import uuid
from os import path
from multiprocessing import Pool
from .linked_structures import Queue, Stack
import datetime
from datetime import timedelta  

class Cache:
    def __init__(self, maxLength=1000):
        self.cacheQueue = Queue[list[dict[str, str | int | bool]]]()
        self.cacheData = {}
        self.cacheSource = {}
        self.maxLength = maxLength
    def __len__(self):
        return self.cacheQueue.size()
    def append(self, cacheID: str, data: list):
        jsonName = cacheID.split("-")[-1]
        print(f"[Cache] jsonName : {jsonName}")
        self.cacheData[cacheID] = data
        self.cacheQueue.enqueue(cacheID)
        if jsonName in self.cacheSource:
            self.cacheSource[jsonName].add(cacheID)
        else:
            self.cacheSource[jsonName] = {cacheID}
        if self.cacheQueue.size() > self.maxLength:
            del self.cacheData[self.cacheQueue.dequeue()]
    def update(self, cacheID: str, data: list):
        if cacheID in self.cacheData:
            self.cacheData[cacheID] = data
        else:
            print(f"Error : CacheID {cacheID} not found")
    def put(self, cacheID: str, data: list):
        if cacheID in self.cacheData:
            self.update(cacheID, data)
        else:
            self.append(cacheID, data)
    def get(self, cacheID):
        if cacheID in self.cacheData:
            return self.cacheData[cacheID]
        else:
            return None
    def deactivate(self, jsonName):
        print(self.cacheSource)
        if jsonName not in self.cacheSource:
            print(f"{jsonName} is not on cache.")
            return
        for cache in self.cacheSource[jsonName]:
            self.cacheData[cache] = {}
    def isValid(self, cacheID):
        if cacheID not in self.cacheData:
            return False
        return self.cacheData[cacheID] != {}

class CollectionService:
    def __init__(self, name, repoPath, jsonSize=100, threadSize=10, CacheLength=10000):
        def mkdir(Path, name):
            fullPath = f"{Path}/{name}"
            if path.exists(fullPath):
                return
            else:
                os.mkdir(fullPath)
        def isExits(Path, name):
            fullPath = f"{Path}/{name}"
            print(fullPath)
            return path.isfile(fullPath)

        self.config = None
        p = f"_{name}.cnfg"
        if isExits(f"{repoPath}/{name}", p):
            self.config = json.loads(open(f"{repoPath}/{name}/{p}", "r").read())
            self.config["jsonAvailable"] = Stack(self.config["jsonAvailable"])
            self.config["threadSize"] = self.threadSize
        else:
            mkdir(repoPath,name)
            self.config = {
                "name" : name,
                "path" : repoPath,
                "jsonSize" : jsonSize,
                "threadSize" : threadSize,
                "CacheLength" : CacheLength,
                "jsonAvailable" : Stack(),
                "allJson" : {},
                "tag" : {}
                }
            self.saveConfig()
        self.whereCache = Cache()
        self.whereCacheIndex = {}
        self.whereCacheValid = {}
        self.jsonCache = {}
        self.jsonValid = {}

    def __len__(self):
        buffer = 0
        for c in self.config["allJson"].keys():
            buffer += self.config["allJson"][c]
        return buffer
    def isCachValid(self, cacheID, validation, cacheBin):
        return cacheID in cacheBin and cacheID in validation and validation[cacheID]
    def saveCache(self, id, Data, validation, cacheBin):
        if len(cacheBin) < self.config["CacheLength"]:
            cacheBin[id] = Data
        else:
            cacheBin.pop()
            validation.pop()
            cacheBin[id] = Data
    def saveConfig(self):
        name = self.config["name"]
        p = f"_{name}.cnfg"
        f = open(f"{self.collectionPath()}/{p}", "w")
        self.config["jsonAvailable"] = self.config["jsonAvailable"].items()
        self.config["tag"]
        f.write(json.dumps(self.config))
        f.close()
        self.config["jsonAvailable"] = Stack(self.config["jsonAvailable"])
    def doConfig(self, param, val):
        self.config[param] = val
        self.saveConfig()
    def collectionPath(self):
        name = self.config["name"]
        path = self.config["path"]
        return f"{path}/{name}"
    def createNewJson(self, jsonName):
        fullPath = f"{self.collectionPath()}/{jsonName}.json"
        if not os.path.isfile(fullPath):
            f = open(f"{self.collectionPath()}/{jsonName}.json", "x")
            f.write(json.dumps({}))
            f.close()
            self.config["jsonAvailable"].push(jsonName)
            self.config["allJson"][jsonName] = 0
            self.saveConfig()
        else:
            print(f"Warning : createNewJson skipped due to exitsing file. file : {fullPath}")
    def loadJson(self, jsonName):
        cacheID = f"{jsonName}"
        cached = cacheID in self.jsonCache
        valid = self.isCachValid(cacheID, self.jsonValid, self.jsonCache)
        if cached and valid:
            print(f"Load {cacheID} from cache")
            return self.jsonCache[cacheID]
        print(f"Loading {jsonName}.json from disk. (loadJson)")
        data = json.load(open(f"{self.collectionPath()}/{jsonName}.json", "r"))
        print(f"Saving {cacheID}.json cache.")
        self.saveCache(cacheID, data, self.jsonValid, self.jsonCache)
        self.jsonValid[cacheID] = True
        return data
        
    def saveJson(self, jsonName, data, tags=None):
        f = open(f"{self.collectionPath()}/{jsonName}.json", "w+")
        f.write(json.dumps(data))
        f.close()
        if tags is not None:
            for tag in tags:
                if tag in self.config["tag"]:
                    self.config["tag"][tag][jsonName] = True
                else:
                    self.config["tag"][tag] = {jsonName: True}
        print("saving")
        self.saveConfig()
        self.saveCache(jsonName, data, self.jsonValid, self.jsonCache)
        print(f"Deactivating {jsonName} qurry cache")
        self.whereCache.deactivate(jsonName)
    def deleteJson(self, jsonName):
        fullPath = f"{self.collectionPath()}/{jsonName}.json"
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    def getJson(self):
        if self.config["jsonAvailable"].isEmpty():
            newName = str(len(self.config["allJson"]))
            self.createNewJson(newName)
            return newName, self.loadJson(newName) 
        else:
            jsonName = self.config["jsonAvailable"].peek()
            return jsonName, self.loadJson(jsonName) 
    def dumpJson(self):
        res = {}
        for jsonName in self.config["allJson"].keys():
            Json = self.loadJson(jsonName)
            for docID in Json.keys():
                res[jsonName] = {"docID" : docID, "Data":Json[docID]}
        return res
    def addDoc(self, data, tags=[None]):
        jsonName, jsonData = self.getJson()
        id = str(uuid.uuid1())+f"_{jsonName}"
        jsonData[id] = data
        jsonData[id]["id"] = id
        jsonData[id]["tags"] = dict.fromkeys(tags, True)
        self.saveJson(jsonName, jsonData, tags=tags)
        self.config["allJson"][jsonName] += 1
        if self.config["allJson"][jsonName] >= self.config["jsonSize"]:
            self.config["jsonAvailable"].pop()
        self.saveConfig()
        return id
    def searchThread(self, jsonName, Json, operator, column, value, tags):
        Bin = []
        if operator == "==":
            for docID in Json.keys():
                if Json[docID][column] == value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == ">=":
            for docID in Json.keys():
                if Json[docID][column] >= value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == "<=":
            for docID in Json.keys():
                if Json[docID][column] <= value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == ">":
            for docID in Json.keys():
                if Json[docID][column] > value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == "<":
            for docID in Json.keys():
                if Json[docID][column] < value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == "!=":
            for docID in Json.keys():
                if Json[docID][column] != value and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == "contain":
            for docID in Json.keys():
                if value in Json[docID][column] and (all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}):
                    Bin.append(Json[docID])
        elif operator == "#":
            for docID in Json.keys():
                if all(tag in Json[docID]["tags"] for tag in tags) or tags == {None}:
                    Bin.append(Json[docID])
        for tag in tags:
            if tag is not None and len(Bin) == 0:
                del self.config["tag"][tag][jsonName]
                if len(self.config["tag"][tag]) == 0:
                    del self.config["tag"][tag]
                self.saveConfig()
        return Bin, jsonName
    def where(self, column, operator, value, tags={None}):
        def getJsons(tags):
            print("---")
            if len(set(tags).intersection(set(self.config["tag"]))) != len(tags):
                return f"Tags {tags} is invalid"
            buffer = set(self.config["tag"][tags[0]])
            for tag in tags[1:]:
                buffer = buffer.intersection(set(self.config["tag"][tag].keys()))
            print(f"set : {buffer}, len : {len(buffer)}")
            return buffer
        res = []
        buffer = []
        cachedData = []
        pool = Pool(processes = self.config["threadSize"] if self.config["jsonAvailable"].size() > self.config["threadSize"] else self.config["jsonAvailable"].size() if self.config["jsonAvailable"].size() != 0 else 1)  
        jsonBin = self.config["allJson"].keys() if tags == {None} else getJsons(tags)
        print(jsonBin)
        if type(jsonBin) == str:
            return jsonBin
        for jsonName in jsonBin:
            if self.config["allJson"][jsonName] == 0:
                continue
            cacheID = f"{operator}-{column}-{str(value)}-{str(tags)}-{jsonName}"
            cached = cacheID in self.whereCache.cacheData
            valid = self.whereCache.isValid(cacheID)
            if cached and valid:
                print(f"Load {cacheID} from cache, Document in cache")
                cachedData.append(self.whereCache.cacheData[cacheID])
                continue
            Json = self.loadJson(jsonName)
            buffer.append(pool.apply_async(self.searchThread, [jsonName, Json, operator, column, value, tags]))
        for ticket in buffer:
            result = ticket.get(timeout=10)
            if len(result) != 0:
                res += result[0]
                cacheID = f"{operator}-{column}-{str(value)}-{str(tags)}-{result[1]}"
                if result[0] != []:
                    self.whereCache.put(cacheID, result[0])
        for cache in cachedData:
            res += cache
        return res
    def getDoc(self, docID):
        jsonName = docID.split("_")[1]
        return self.loadJson(jsonName)[docID]
    def findToDeleteThread(self, Json, DocId, jsonName):
            for Id in Json.keys():
                if DocId == Id:
                    return [jsonName, Id]
            return []
    def deleteDoc(self, docID):
        jsonName = docID.split("_")[1]
        Json = self.loadJson(jsonName)
        if docID not in Json:
            print(f"[deleteDoc] docID {docID} not found in { jsonName}")
            return
        print(f"Deleting : {docID}")
        del Json[docID]
        self.config["allJson"][jsonName] -= 1
        if jsonName not in self.config["jsonAvailable"].items():
            self.config["jsonAvailable"].push(jsonName)
        self.saveJson(jsonName, Json)
        self.saveConfig()
    def updateDoc(self, docID, data):
        jsonFile = self.loadJson(docID.split("_")[1])
        jsonFile[docID] = data
        self.saveJson(docID.split("_")[1], jsonFile)
    def removeTag(self, docID, tag):
        doc = self.getDoc(docID)
        if tag in doc["tags"]:
            del doc["tags"][tag]
            self.updateDoc(doc["id"], doc)
            return
        print(f"[removeTag] tag {tag} not found in {docID}")
    def addTag(self, docID, tag):
        doc = self.getDoc(docID)
        doc["tags"][tag] = True
        self.updateDoc(doc["id"], doc)
        if tag in self.config["tag"]:
            self.config["tag"][tag][str(doc["id"].split("_")[1])] = True
        else:
            self.config["tag"][tag] = {str(doc["id"].split("_")[1]) : True}
        self.saveConfig()
        print(f"[addTag] tag {tag} not found in {docID}")


        
class LogService():
    def __init__(self, name, repoPath, jsonSize=100, maxLogAge=30):
        self.logDB = CollectionService(self, name, repoPath, jsonSize, threadSize=10, CacheLength=1000)
        self.maxAge = maxLogAge
    def push(self, data, Date, tags=[]):
        date, time = Date.split(" ")
        d,m,y = date.split("/")
        h,m = time.split(".")
        data["timeStamp"] = Date
        self.logDB.addDoc(data, [d+"d", m+"m", y+"y", h+"h", m+"m"]+tags)
    def removeOutdate(self):
        i = self.maxAge
        while True:
            p = datetime.datetime.now() - timedelta(days=i)
            outdated = self.logDB.where("id","#",True,[f"{p.day}d",f"{p.month}",f"{p.year}"])
            if len(outdated) == 0:
                break
            for doc in outdated:
                self.logDB.deleteDoc(doc["id"])
            i += 1

    