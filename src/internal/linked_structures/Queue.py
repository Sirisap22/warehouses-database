from collections import deque
from typing import Iterable, Optional, Any, Generic, TypeVar

T = TypeVar("T")

class Queue(Generic[T]):
    def __init__(self, lis: Optional[Iterable[T]]=None) -> None:
        if lis is None:
            self.store = deque()
        else:
            self.store = deque(lis)

    def __str__(self) -> str:
        return str(self.store)

    def isEmpty(self) -> bool:
        return len(self.store) == 0
    
    def size(self) -> int:
        return len(self.store)
    
    def items(self) -> list[T]:
        return list(self.store)

    def peek(self) -> T:
        return self.store[0]

    def enqueue(self, data: Any) -> None:
        self.store.append(data)

    def dequeue(self) -> T:
        return self.store.popleft()



