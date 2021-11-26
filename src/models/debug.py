from pydantic import BaseModel

class UpdateItemsCountData(BaseModel):
    path: str
    count: int