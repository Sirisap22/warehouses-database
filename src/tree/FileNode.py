from .TreeNode import TreeNode

class FileNode(TreeNode):
    def __init__(self, data: str):
        super().__init__(data, None)