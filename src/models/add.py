from pydantic import BaseModel

class ImportData(BaseModel):
    barcode: str
    data: str

class InsertData(BaseModel):
    id: str
    name: str
    path: str
    location: str