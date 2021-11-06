from __future__ import annotations
from typing import Optional

class TreeNode:
    def __init__(self, data: str, children: Optional[list[TreeNode]]=[]) -> None:
        self.data = data
        self.children = children
    
    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

class WarehousesTree:
    def __init__(self, root: TreeNode) -> None:
        self.root = root

    def __str__(self):
        queue = [self.root]
        s = []
        while len(queue) != 0:
            cur = queue.pop(0)
            s.append(str(cur))
            if cur is None or cur.children is None:
                continue
            for child in cur.children:
                s.append(str(child))
            s.append('||')
        return str(s)
            
    def traverse(self, path) -> TreeNode | None:
        ways = path.split('/')

        #TODO Optimaize traverse time
        destinationNode = self.root
        for way in ways:
            for child in destinationNode.children:
                if child.data == way:
                    destinationNode = child
                    break
            
            # never reach if reach then some way in path do not exist.
            return None
        
        return destinationNode
    
    def parent(self, path) -> TreeNode | None:
        ways = path.split('/')[:-1]

        #TODO Optimaize traverse time
        parentNode = self.root
        for way in ways:
            for child in parentNode.children:
                if child.data == way:
                    parentNode = child
                    break

            # never reach if reach then some way in path do not exist.
            return None
        
        return parentNode
    
    def checkDuplicate(self, node: TreeNode, data):
        ''' Check in the children of a given {node} if there an exist TreeNode that the data is equal to {data}'''
        if node.children is None or len(node.children) == 0:
            return False

        for child in node.children:
            if child.data == data:
                return True
        
        return False

    def insertNonItem(self, path: str, nonItem: str) -> TreeNode | None:
        destinationNode = self.traverse(path)
        # if destinationNode.isLeaf():
        #     return None
        
        destinationNode.children.append(TreeNode(nonItem, []))
        return destinationNode[-1]
    
    def insertItem(self, path: str, data: str) -> TreeNode | None:

        destinationNode = self.traverse(path)
        # if destinationNode.isLeaf():
        #     return None

        destinationNode.children.append(TreeNode(data))
        return destinationNode[-1]

    def insertMultipleItems(self, path: str, data: str) -> TreeNode | None:

        destinationNode = self.traverse(path)
        # if destinationNode.isLeaf():
        #     return None

        destinationNode.children = destinationNode.children + list(map(lambda data: TreeNode(data)))
        return destinationNode[-1]

    def delete(self, path: str, deleteItem: str) -> TreeNode | None:
        parentNode = self.traverse(path)
        parentNode.children = list(filter(lambda child: child.data != deleteItem, parentNode.children))
    
    def deleteMultiple(self, path: str, deleteItems) -> TreeNode | None:
        parentNode, destinationItem = self.traverse(path)
        parentNode.children = list(filter(lambda child: child.data not in deleteItems, parentNode.children))


            




    