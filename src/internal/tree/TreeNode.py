from __future__ import annotations
from typing import Optional, Type

class TreeNode:
    def __init__(self, data: str, children: Optional[dict[str, Type[TreeNode]]]):
        self.data = data
        self.children = children
    
    def __str__(self) -> str:
        return str(self.data)
    
    def jsonable(self):
        return self.__dict__