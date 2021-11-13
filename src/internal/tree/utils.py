from typing import Type, Any, Type
from dotenv import dotenv_values
import json

from .TreeNode import TreeNode
from .FolderNode import FolderNode
from .NavigateTree import NavigateTree
from .TreeNode import TreeNode
from ..linked_structures import Queue

config = dotenv_values('.env')

def breathFirstSearchLimit(root: FolderNode, maxDepth: int = 1):
    if maxDepth > 2:
        return {}
    curDepth = 0

    search = {}
    queue = Queue([(root, search)])
    depthTrack = [1]
    d_idx = 0
    while not queue.isEmpty() and curDepth < maxDepth:
        curRoot, curSearch = queue.deque()
        if curRoot is None:
            continue

        if curRoot.children is not None:
            if len(depthTrack) <= d_idx+1:
                depthTrack.append(0)
            depthTrack[d_idx+1] += len(curRoot.children.keys())

        for _, child in curRoot.children.items():
            type, name, id = child.data.split(config['FLAG'])

            if isinstance(child, FolderNode):
                curSearch[type+config['FLAG']+name] = {}
                queue.enqueue((child, curSearch[type+config['FLAG']+name]))
            else:
                curSearch[type+config['FLAG']+name] = None

        depthTrack[d_idx] -= 1
        if depthTrack[d_idx] == 0:
            d_idx += 1
            curDepth += 1

    return search

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

    



