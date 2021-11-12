from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import dotenv_values
import uvicorn
from datetime import datetime

from .internal import TreeService, NodeType, treeToJSON, MetaData, MetaType, CollectionService, BarcodeService
from .models.search import InsertPath, DeletePath, DeleteItemList
from .models.add import InsertData

config = dotenv_values('.env.dev')

app = FastAPI()

origins = [config["ORIGIN"]]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

treeService = TreeService("tree", config['PATH'])
collectionService = CollectionService("warehouseDB", config['PATH'], CacheLength=1000000)
barcodeService = BarcodeService("barcode", config['PATH'])

@app.on_event("shutdown")
def shutdown_event():
    treeService.saveObject()

@app.get("/", tags=["search"])
async def getHome():
    return Response(media_type="application/json", content=treeToJSON(treeService.navigationTree.root))

@app.get("/warehouse", tags=["search"])
async def getWarehouse():
    return treeService.getWarehouses()

@app.get("/warehouse/{warehouseName}/zone/{zoneName}", tags=["search"])
async def getShelfs(warehouseName: str, zoneName: str):
    return treeService.getShelfs(f"warehouse{warehouseName}/zone{zoneName}")

@app.get("/warehouse/{warehouseName}/zone/{zoneName}/shelf/{shelfName}", tags=["search"])
async def getItems(warehouseName: str, zoneName: str, shelfName: str):
    itemsId = treeService.getItems(f"warehouse{warehouseName}/zone{zoneName}/shelf{shelfName}")
    res = []
    for Id in itemsId:
        res.append(collectionService.getDoc(Id))
    return res

@app.post("/path", tags=["search"])
async def insertPath(insertPath: InsertPath):
    metaData = {
        "type": insertPath.type,
        "name": insertPath.name,
        "id": insertPath.name,
    }

    return treeService.insert(NodeType.NON_ITEM, insertPath.path, metaData)

@app.delete("/path", tags=["search"])
async def deletePath(deletePath: DeletePath):
    return treeService.delete(NodeType.NON_ITEM, deletePath.path, deletePath.nameList)


@app.get("/holding-items", tags=["add"])
async def getHoldingItems():
    holdingItems = collectionService.where("id","#",True, tags=["holding-items"])

    itemsData = []
    for holdingItem in holdingItems:
        itemsData.append(barcodeService.mapBarcode(holdingItem['barcode'])['name'])

    processedHoldingItems = []
    for holdingItem, itemData in zip(holdingItems, itemsData):
        processedHoldingItems.append({
            "id": holdingItem['id'],
            "date": holdingItem['date'],
            "name": itemData
        })
    
    return processedHoldingItems

@app.post("/holding-items", tags=["add"])
async def importItem(barcodeList: list[str]):
    try:
        products = []
        for barcode in barcodeList:
            products.append(barcodeService.mapBarcode(barcode))

        for barcode, product in zip(barcodeList, products):
            collectionService.addDoc({
                "barcode": barcode,
                "date": datetime.now().isoformat()
            }, tags=[barcode, "holding-items"])
        
        return True
    except:
        return False

@app.get("/item/{itemId}", tags=["search"])
async def getItemById(itemId: str):
    doc = collectionService.getDoc(itemId)
    itemData = barcodeService.mapBarcode(doc["barcode"])
    res = {
        **itemData,
        **doc
    }

    del res["barcode"]
    del res["tags"]
    del res["tag"]

    return res

@app.post("/item", tags=["add"])
async def insertItem(insertData: InsertData):
    try:
        doc = collectionService.getDoc(insertData.id)
        doc["path"] = insertData.path
        doc["location"] = insertData.location
        doc["date"] = datetime.now().isoformat()

        if "holding-items" in doc["tags"]:
            del doc["tags"]["holding-items"]
        collectionService.updateDoc(insertData.id, doc)


        treeService.insert(NodeType.ITEM, insertData.path, {
            "name": insertData.name,
            "id": doc["id"],
            "type": MetaType.ITEM
        })

        return True
    except:
        return False

@app.delete("/item", tags=["search"])
async def deleteItem(deleteItemList: DeleteItemList):
    # try:
        treeService.deleteMultiple(NodeType.ITEM, deleteItemList.path, deleteItemList.itemIdList)
        for id in deleteItemList.itemIdList: 
            collectionService.deleteDoc(id)
        return True
    # except:
    #     return False

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=f'{config["HOST"]}', port=int(config["PORT"]), reload=False)