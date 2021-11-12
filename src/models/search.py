from pydantic import BaseModel

class InsertPath(BaseModel):
    path: str
    type: str
    name: str

class DeletePath(BaseModel):
    path: str
    nameList: list[str]