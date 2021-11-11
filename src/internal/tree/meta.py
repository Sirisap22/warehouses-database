from typing import TypedDict
from enum import Enum

class MetaType(Enum):
    def __str__(self):
        return str(self.value)
    def jsonable(self):
        return self.__str__()
    WAREHOUSE: str = 'warehouse'
    ZONE: str = 'zone'
    SHELF: str = 'shelf'
    ITEM: str = ''

class MetaData(TypedDict):
    name: str
    type: MetaType
    id: str