from .TreeNode import TreeNode
from .meta import MetaData

class FileNode(TreeNode):
    def __init__(self, data: MetaData):
        super().__init__(data, None)