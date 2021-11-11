from __future__ import annotations
from typing import Optional, Type
from .meta import MetaData

class TreeNode:
    def __init__(self, data: MetaData, children: Optional[dict[str, Type[TreeNode]]]):
        self.data = data
        self.children = children
    
    def __str__(self) -> str:
        return str(self.data['type']+self.data['name'])
    
    def jsonable(self):
        return self.__dict__