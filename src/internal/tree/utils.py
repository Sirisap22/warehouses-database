from typing import Type
from collections import deque
import json

from .FolderNode import FolderNode
from .NavigateTree import NavigateTree
from .TreeNode import TreeNode
from ..linked_structures import Queue

def breathFirstSearch(root: FolderNode, depth: int):
    queue = Queue()
    pass

def printNavigateTreeByDepth(tree: NavigateTree) -> None:
    print('[\'root\']')

    q = []
    qn = []
    depthTrack = [len(tree.root.children.keys())]
    d_idx = 0
    print(list(map(lambda k: f'root/{k}', tree.root.children.keys())))
    for key, value in tree.root.children.items():
        q.append((key, value))

    while len(q) != 0:
        parent, cur = q.pop(0)

        if not cur.children is None:
            q.extend(cur.children.items())
            qn.extend(list(map(lambda k: f'{parent}/{k}', cur.children.keys())))

            if len(depthTrack) <= d_idx+1:
                depthTrack.append(0)
            depthTrack[d_idx+1] += len(cur.children.keys())

        depthTrack[d_idx] -= 1
        if depthTrack[d_idx] == 0:
            d_idx += 1
            print(qn)
            qn.clear()

def complexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))

def treeToJSON(root: Type[TreeNode]) -> str:
    if root.children is None:
        return json.dumps({})
    
    return json.dumps(root, default=complexHandler)

def childrenToJSON(root: Type[TreeNode]) -> str:
    if root.children is None:
        return json.dumps({})
    
    return json.dumps(list(root.children.keys()), default=complexHandler)

    



