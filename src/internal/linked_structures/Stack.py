from __future__ import annotations
from collections import deque
from typing import Iterable, Optional, Any, Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self, lis: Optional[Iterable[T]]=None) -> None:
        if lis is None:
            self.store = deque()
        else:
            self.store = deque(lis)

    def __str__(self) -> str:
        return str(self.store)

    def peek(self) -> T:
        return self.store[-1]

    def push(self, data: Any) -> None:
        self.store.append(data)

    def pop(self) -> T:
        return self.store.pop()