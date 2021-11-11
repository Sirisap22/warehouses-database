from .TreeNode import TreeNode
from .meta import MetaData

class FolderNode(TreeNode):
    def __init__(self, data: MetaData):
        super().__init__(data, {})