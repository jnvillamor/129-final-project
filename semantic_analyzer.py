# Import necessary modules
import ast

class SemanticAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}

    def visit_Assign(self, node):
        # Handle variable assignments
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = node.value
        self.generic_visit(node)

    def visit_Name(self, node):
        # Check for undeclared variables
        if isinstance(node.ctx, ast.Load) and node.id not in self.variables:
            print(f"Semantic Error: Undeclared variable '{node.id}' at line {node.lineno}")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Check for type mismatches in binary operations
        left_type = self.get_type(node.left)
        right_type = self.get_type(node.right)
        if left_type != right_type:
            print(f"Semantic Error: Type mismatch in binary operation at line {node.lineno}")
        self.generic_visit(node)

    def get_type(self, node):
        # Simplified type inference
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.Name) and node.id in self.variables:
            return type(self.variables[node.id]).__name__
        return None

def analyze_code(source_code):
    tree = ast.parse(source_code)
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)

if __name__ == "__main__":
    # Example usage
    code = """
x = 10
y = 'hello'
z = x + y
"""
    analyze_code(code) 