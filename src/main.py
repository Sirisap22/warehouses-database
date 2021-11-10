from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import dotenv_values
import uvicorn

from .internal import TreeService, NodeType, treeToJSON, MetaData
from .models.search import InsertPath

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

treeService = TreeService("tree", f"{config['TREE_PATH']}")

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
    return treeService.getItems(f"warehouse{warehouseName}/zone{zoneName}/shelf{shelfName}")

@app.post("/path", tags=["search"])
async def insertPath(insertPath: InsertPath):
    metaData = {
        "type": insertPath.type,
        "name": insertPath.name,
        "id": insertPath.name,
    }
    return treeService.insert(NodeType.NON_ITEM, insertPath.path, metaData)



if __name__ == "__main__":
    uvicorn.run("src.main:app", host=f'{config["HOST"]}', port=int(config["PORT"]), reload=False)