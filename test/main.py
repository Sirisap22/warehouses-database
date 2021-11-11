import asyncio
from fastapi import FastAPI
from src.internal.CollectionService import CollectionService
from pydantic import BaseModel
import uvicorn

class Student(BaseModel):
    name: str
    age: int
    years: int



app = FastAPI()
db = CollectionService("apitest", "D:", jsonSize=100, threadSize=60, CacheLength=10000)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/cache")
async def cache():
    return f""" Search cache : {len(db.whereCache)}, JSON cache : {len(db.jsonCache)}  {db.whereCache.cacheData}  {db.jsonCache}"""

@app.get("/valid")
async def cache():
    return f"{db.whereCacheValid} {db.jsonValid}"

@app.get("/student")
async def student():
    return db.where("ID", "#", True)

@app.get("/student/id/{id}")
async def student(id: str):
    return db.getDoc(id)

@app.get("/student/len")
async def student():
    return len(db)

@app.get("/student/len/{tags}")
async def student(tags: str):
    return len(db.where("ID","#",True, tags=tags.split("-")))

@app.get("/student/{years}")
async def getByYears(years: int):
    return db.where("years", "==", years)

@app.get("/student/name/{name}")
async def getByName(name: str):
    return db.where("name", "==", name)

@app.get("/student/name/{name}/{tag}")
async def getByName(name: str, tag: str):
    return db.where("name", "==", name, tags=tag.split("-"))

@app.get("/student/ageOver/{years}")
async def getByYears(years: int):
    return db.where("age", ">=", years)

@app.get("/student/age/{years}")
async def getByYears(years: int):
    return db.where("age", "==", years)

@app.get("/student/notAge/{years}")
async def getByYears(years: int):
    return db.where("age", "!=", years)

@app.get("/student/ageUnder/{years}")
async def getByYears(years: int):
    return db.where("age", "<=", years)

@app.get("/student/countYears/{years}")
async def getByYears(years: int):
    return len(db.where("years", "==", years))

@app.get("/student/tag/{tag}")
async def register(tag: str):
    data = db.where("ID", "#", True, tags=tag.split("-"))
    return data

@app.post("/student/tag/{tag}")
async def register(student: Student, tag: str):
    db.addDoc(student.dict(), tags=tag.split("-"))
    print(student)
    return 200

@app.delete("/student/remove/{name}")
async def delete_student(name: str):
    doc = db.where("name", "==", name)
    print(doc)
    if len(doc) != 0:
        db.deleteDoc(doc[0]["ID"])
    return doc

@app.delete("/student/removeDummy")
async def delete_dummy():
    doc = db.where("name", "contain", "JackD")
    # print(f"dummy : {len(doc)}, {doc}")
    for d in doc:
        # print(d)
        db.deleteDoc(d["ID"])
    return len(doc)

@app.delete("/student/removeByYears/{years}")
async def deleteByYears(years: int):
    doc = db.where("years", "==", years)
    # print(f"dummy : {len(doc)}, {doc}")
    for d in doc:
        # print(d)
        db.deleteDoc(d["ID"])
    return len(doc)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)