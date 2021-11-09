from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import dotenv_values
import uvicorn

from .internal import TreeService, NodeType, treeToJSON
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

@app.get("/warehouse", tags=["search"])
async def getHome():
    return Response(media_type="application/json", content=treeToJSON(treeService.navigationTree.root))

@app.post("/path", tags=["search"])
async def insertPath(insertPath: InsertPath):
    metaData = {
        "name": insertPath.name,
        "id": insertPath.name,
    }
    return treeService.insert(NodeType.NON_ITEM, insertPath.path, metaData)



if __name__ == "__main__":
    uvicorn.run("src.main:app", host=f'{config["HOST"]}', port=int(config["PORT"]), reload=False)