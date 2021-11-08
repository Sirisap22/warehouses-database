import json
import os
import uuid
from os import path
from multiprocessing import Pool

class Stack:
    def __init__(self, list = None):
        if list == None:
            self.items = []
        else:
            self.items = list

    def __str__(self):
        s = 'stack of '+ str(self.size())+' items : '
        for ele in self.items:
            s += str(ele)+' '
        return s
    def parseJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def push(self, i):
        self.items.append(i)

    def pop(self):   #edit code
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

# class QueueCache:
#     def __init__(self, maxLength):
#         self.items = {}
#         self.maxLength = maxLength

#     def __len__(self):
#         return len(self.items)
#     def __str__(self):
#         return str(self.items)
#     def __getitem__(self, key):
#         item = self.items[key]
#         del self.items[key]
#         self.enQueue(key, item)
#         return self.items[key]
#     def lastKey(self):
#         return list(self.items.keys())[0]
#     def enQueue(self, key, data):
#         self.items[key] = data
#         if len(self.items) > self.maxLength:
#             self.deQueue()
#     def deQueue(self):
#         if len(self.items) != 0:
#             res = {self.lastKey() : self.items[self.lastKey()]}
#             del self.items[self.lastKey()]
#             return res
#         return {}
#     def peek(self):
#         return self.items[self.lastKey()]
#     def size(self):
#         return sys.getsizeof(self.items)
#     def available(self, key):
#         isContain = self.items[key] is not None 
#         if isContain:
#             item = self.items[key]
#             del self.items[key]
#             self.enQueue(key, item)
#         return isContain
#     def update(self, key, data):
#         self.items[key] = data

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
        self.whereCache = {}
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
    def saveCache(self, ID, Data, validation, cacheBin):
        # print(f"Saving cache for {ID}")
        if len(cacheBin) < self.config["CacheLength"]:
            cacheBin[ID] = Data
        else:
            # print("Cache overflow")
            cacheBin.pop()
            validation.pop()
            cacheBin[ID] = Data
    def saveConfig(self):
        name = self.config["name"]
        p = f"_{name}.cnfg"
        f = open(f"{self.collectionPath()}/{p}", "w")
        self.config["jsonAvailable"] = self.config["jsonAvailable"].items
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
            # print(self.jsonCache[cacheID])
            return self.jsonCache[cacheID]
        print(f"Loading {jsonName}.json from disk. (loadJson)")
        data = json.load(open(f"{self.collectionPath()}/{jsonName}.json", "r"))
        # self.cache.enQueue(jsonName, data)
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
        # for cacheID in list(self.whereCache.keys()):

        #     jName = cacheID.split("-")[-1]
        #     if jName == jsonName:
        #         # print(f"{jName}.json is not valid anymore.")
        #         self.saveCache(cacheID, data, self.jsonValid, self.jsonCache)
        #         self.jsonValid[cacheID] = False
        # if self.cache.available(jsonName):
        #     self.cache.update(jsonName, data)
    def deleteJson(self, jsonName):
        fullPath = f"{self.collectionPath()}/{jsonName}.json"
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    def getJson(self):
        # for jsonName in self.config["jsonAvailable"].keys():
        #     if self.config["jsonAvailable"][jsonName] < self.config["jsonSize"]:
        #         return jsonName, self.loadJson(jsonName)
        # newName = str(len(self.config["jsonAvailable"]))
        # self.createNewJson(newName)
        # return newName, self.loadJson(newName)
        if self.config["jsonAvailable"].isEmpty():
            newName = str(len(self.config["allJson"]))
            self.createNewJson(newName)
            return newName, self.loadJson(newName) 
        else:
            jsonName = self.config["jsonAvailable"].peek()
            # if self.cache.available(jsonName):
            #     data = self.cache[jsonName]
            #     return jsonName, data
            # else:
            # data = json.load(open(f"{self.collectionPath()}/{jsonName}.json", "r"))
            # self.cache.enQueue(jsonName, data)
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
        ID = str(uuid.uuid1())+f"_{jsonName}"
        jsonData[ID] = data
        jsonData[ID]["ID"] = ID
        jsonData[ID]["tags"] = tags
        self.saveJson(jsonName, jsonData, tags=tags)
        self.config["allJson"][jsonName] += 1
        if self.config["allJson"][jsonName] >= self.config["jsonSize"]:
            self.config["jsonAvailable"].pop()
        self.saveConfig()
        return ID
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
            print(f"set : {buffer}")
            return buffer
        res = []
        buffer = []
        chachedData = []
        pool = Pool(processes = self.config["threadSize"] if self.config["jsonAvailable"].size() > self.config["threadSize"] else self.config["jsonAvailable"].size() if self.config["jsonAvailable"].size() != 0 else 1)  
        jsonBin = self.config["allJson"].keys() if tags == {None} else getJsons(tags)
        print(jsonBin)
        if type(jsonBin) == str:
            return jsonBin
        # list(self.config["tag"][tag].keys())
        for jsonName in jsonBin:
            # print(jsonName)
            if self.config["allJson"][jsonName] == 0:
                continue
            # cacheID = f"{operator}-{column}-{str(value)}-{jsonName}"
            # cached = cacheID in self.whereCache
            # valid = self.isCachValid(cacheID, self.whereCacheValid, self. whereCache)
            # if cached and valid:
            #     print(f"Load {cacheID} from cache, Document in cache : {len(self.whereCache[cacheID])}, Search cache :{len(self.whereCache)}")
            #     # print(self.whereCache[cacheID])
            #     chachedData.append(self.whereCache[cacheID])
            #     continue
            Json = self.loadJson(jsonName)
            buffer.append(pool.apply_async(self.searchThread, [jsonName, Json, operator, column, value, tags]))
            # t = multiprocessing.Process(target=self.searchThread, args=(Json, res, operator, column, value))
            # t.start()
            # threads.append(t)
            # while len(threads) >= self.config["threadSize"]:
            #     continue
                # garbage = []
                # for threadInd in range(len(threads)):
                #     if not threads[threadInd].is_alive():
                #         garbage.append(threadInd)
                # for threadInd in garbage:
                #     del threads[threadInd]
        # for thread in threads:
        #     thread.join()
        for ticket in buffer:
            result = ticket.get(timeout=10)
            if len(result) != 0:
                res += result[0]
                # cacheID = f"{operator}-{column}-{str(value)}-{result[1]}"
                # if result[0] != []:
                #     self.saveCache(cacheID, result[0], self.whereCacheValid, self.whereCache)
                # self.whereCacheValid[cacheID] = True
        for cache in chachedData:
            res += cache
        return res
    def getDoc(self, docID):
        jsonName = docID.split("_")[1]
        return self.loadJson(jsonName)[docID]
    def findToDeleteThread(self, Json, DocId, jsonName):
            for Id in Json.keys():
                if DocId == Id:
                    # print(f"Found : {Id}")
                    return [jsonName, Id]
            return []
    def deleteDoc(self, docID):
        # deleteList = []
        # buffer = []
        # pool = Pool(processes=self.config["threadSize"])
        # for jsonName in self.config["allJson"].keys():
        #     if self.config["allJson"][jsonName] == 0:
        #         continue
        #     print(f"Searching in {jsonName}.json")
        #     Json = self.loadJson(jsonName)
        #     # threads.append(multiprocessing.Process(target=self.findToDeleteThread, args=(Json, docID, deleteList, jsonName)))
        #     # threads[-1].start()
        #     buffer.append(pool.apply_async(self.findToDeleteThread, [Json, docID, jsonName]))
        # # for thread in threads:
        # #     thread.join()
        # for ticket in buffer:
        #     result = ticket.get(timeout=1)
        #     if result != None and len(result) != 0:
        #         deleteList = result
        jsonName = docID.split("_")[1]
        Json = self.loadJson(jsonName)
        print(f"Deleting : {docID}")
        del Json[docID]
        self.config["allJson"][jsonName] -= 1
        if jsonName not in self.config["jsonAvailable"].items:
            self.config["jsonAvailable"].push(jsonName)
        self.saveJson(jsonName, Json)
        self.saveConfig()
        
class MockupDB:
    def __init__(self):
        self.colume = []