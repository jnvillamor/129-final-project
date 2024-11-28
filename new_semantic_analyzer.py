class NewSemanticAnalyzer:
    def __init__(self):
        self.variables = {}
        self.errors = []

    def analyze_tokens(self, tokens):
        """
        Analyzes a list of tokens for semantic errors.
        :param tokens: List of tuples (token_type, token_value, line_number)
        """
        for i, (token_type, token_value, line_number) in enumerate(tokens):
            if token_type == "keyword":
                if token_value in ["INT", "STR"]:
                    self._check_variable_declaration(tokens, i, line_number)
                elif token_value == "BEG":
                    self._check_beg_operation(tokens, i, line_number)
                elif token_value in ["MULT", "ADD", "SUB", "DIV", "MOD"]:
                    self._check_operation(tokens, i, line_number)

    def _check_variable_declaration(self, tokens, index, line_number):
        # Check if the next token is a valid variable name
        if index + 1 < len(tokens):
            next_token_type, next_token_value, _ = tokens[index + 1]
            if next_token_type != "variable":
                self.errors.append(f"Semantic Error: Expected variable name after {tokens[index][1]} at line {line_number}")
            else:
                # Store the variable with its type
                self.variables[next_token_value] = tokens[index][1]
        else:
            self.errors.append(f"Semantic Error: Incomplete variable declaration at line {line_number}")

    def _check_beg_operation(self, tokens, index, line_number):
        # Check if the next token is a valid variable name and the input type matches
        if index + 1 < len(tokens):
            next_token_type, next_token_value, _ = tokens[index + 1]
            if next_token_type != "variable" or next_token_value not in self.variables:
                self.errors.append(f"Semantic Error: Undeclared variable after BEG at line {line_number}")
            else:
                # Check if the input type matches the variable type
                if index + 2 < len(tokens):
                    input_type, _, _ = tokens[index + 2]
                    if input_type != self.variables[next_token_value]:
                        self.errors.append(f"Semantic Error: Type mismatch for BEG operation on variable '{next_token_value}' at line {line_number}")
                else:
                    self.errors.append(f"Semantic Error: Missing input type for BEG operation at line {line_number}")
        else:
            self.errors.append(f"Semantic Error: Incomplete BEG operation at line {line_number}")

    def _check_operation(self, tokens, index, line_number):
        # Check if the next two tokens are valid variables and of the same type
        if index + 2 < len(tokens):
            first_operand_type, first_operand_value, _ = tokens[index + 1]
            second_operand_type, second_operand_value, _ = tokens[index + 2]
            if first_operand_type != "variable" or second_operand_type != "variable":
                self.errors.append(f"Semantic Error: Invalid operands for operation at line {line_number}")
            elif self.variables.get(first_operand_value) != self.variables.get(second_operand_value):
                self.errors.append(f"Semantic Error: Type mismatch in operation at line {line_number}")
        else:
            self.errors.append(f"Semantic Error: Incomplete operation at line {line_number}")

    def get_errors(self):
        return self.errors