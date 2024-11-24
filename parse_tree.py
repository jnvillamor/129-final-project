class ParseTreeNode:
    def __init__(self, value, node_type="non-terminal"):
        self.value = value
        self.children = []
        self.parent = None
        self.node_type = node_type  # Can be "non-terminal", "terminal", or "epsilon"

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def get_siblings(self):
        if self.parent is None:
            return []
        return [child for child in self.parent.children if child != self]

class ParseTree:
    def __init__(self):
        self.root = None
        self.current_node = None

    def set_root(self, value):
        self.root = ParseTreeNode(value)
        self.current_node = self.root

    def add_node(self, value, node_type="non-terminal"):
        if self.root is None:
            self.set_root(value)
            return self.root

        new_node = ParseTreeNode(value, node_type)
        self.current_node.add_child(new_node)
        return new_node

    def move_to(self, node):
        self.current_node = node

    def move_up(self):
        if self.current_node.parent:
            self.current_node = self.current_node.parent

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        
        print("  " * level + f"|_{node.value} ({node.node_type})")
        for child in node.children:
            self.print_tree(child, level + 1) 