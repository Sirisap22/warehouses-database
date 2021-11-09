from pydantic import BaseModel

class InsertPath(BaseModel):
    path: str
    name: str
