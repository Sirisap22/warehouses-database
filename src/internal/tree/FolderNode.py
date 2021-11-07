from .TreeNode import TreeNode

class FolderNode(TreeNode):
    def __init__(self, data: str):
        super().__init__(data, {})