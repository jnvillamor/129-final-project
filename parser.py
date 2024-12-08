from symbol_table import SymbolTable # Import the SymbolTable class

class Parser: 
  """
    A class to represent a parser object.
  """
  def __init__(self, symbol_table: SymbolTable):
    self.prod_table = [] # Production table for given IOL
    self.parse_table = [] # Parse table for given IOL
    self.symbol_table = symbol_table # Symbol table object

    # NRPP components
    self.stack = [] # Stack for the parser
    self.input_buffer = [] # Input buffer for the parser
    self.total_output = [] # Total output of the parser

    self.is_valid = bool # Flag to check if overall parsing is valid
    self.errors = [] # List of errors

    self.line_number = 1 # Line number of the input code

    # Semantic Analysis components
    self.arithmetic_operators = ["ADD", "SUB", "MULT", "DIV", "MOD"]  
    self.operation_stack_index = 0
    self.operation_stack = []

    self.in_declaration = False # Flag to check if the parser is in declaration
    self.declaration_stack = []
    self.declaration_line = 0

    self.in_assignment = False # Flag to check if the parser is in assignment
    self.assignment_stack = []
    self.in_assignment_line = 0

    self._getProdTable();
    self._getParseTable()

  def _getProdTable(self):
    """
      Get the production table from the input file named grammar.prod in the current working directory.
    """
    try:
      with open("grammar.prod", "r", encoding="UTF-8") as file: 
        lines = file.readlines()
        for line in lines:
          # Split each line into tokens and strip whitespace
          production = line.strip().split(',')
          self.prod_table.append(production)
        
    except FileNotFoundError:
      print("Error: grammar.prod file not found")
    except Exception as e:
      print(f"Error reading grammar.prod: {str(e)}")

  def _getParseTable(self):
    """
      Get the parse table from the input file named grammar.ptbl in the current working directory.
    """
    try:
      with open("grammar.ptbl", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
          # Split each line into tokens and strip whitespace
          production = line.strip().split(',')
          self.parse_table.append(production)
      
    except FileNotFoundError:
      print("Error: grammar.ptbl file not found")
    except Exception as e:
      print(f"Error reading grammar.ptbl: {str(e)}")

  def _getParseTableRow(self, symbol: str):
    """
      Get the row of the parse table corresponding to the given symbol.
    """
    for ind, X in enumerate(self.parse_table):
      if X[0] == symbol:
        return ind

  def _getParseTableCol(self, symbol: str):
    """
      Get the column of the parse table corresponding to the given symbol.
    """
    for ind, X in enumerate(self.parse_table[0]):
      if X == symbol:
        return ind

  def _getOperationStackNextToken(self):
    """
      Get the next token in the operation stack.
    """
    self.operation_stack_index += 1
    return self.operation_stack[self.operation_stack_index - 1]

  def _expressionSemanticAnalysis(self):
    """
      Perform semantic analysis on the expression.
    """
    operator = self._getOperationStackNextToken()

    # Check if the op1 is expression
    op1 = self._getOperationStackNextToken() 
    if (op1["name"] in self.arithmetic_operators): # If the token is an operator, perform semantic analysis on the expression
      self.operation_stack_index -= 1
      op1_type = self._expressionSemanticAnalysis()
    elif (op1["name"] == "IDENT"): # If the token is an identifier, get the type from the symbol table
      variable = self.symbol_table.get_symbol(op1["value"])
      op1_type = variable["type"]
    else: # If the token is an integer literal, set the type to INT
      op1_type = "INT"

    # Check if the op1 is expression
    op2 = self._getOperationStackNextToken()
    if (op2["name"] in self.arithmetic_operators): # If the token is an operator, perform semantic analysis on the expression
      self.operation_stack_index -= 1
      op2_type = self._expressionSemanticAnalysis()
    elif (op2["name"] == "IDENT"): # If the token is an identifier, get the type from the symbol table
      variable = self.symbol_table.get_symbol(op2["value"])
      op2_type = variable["type"]
    else: # If the token is an integer literal, set the type to INT
      op2_type = "INT"

    return "INT" if (op1_type == "INT" and op2_type == "INT") else "STR" # Return the resulting type of the expression

  def _varDeclarationSemanticAnalysis(self):
    """
      Perform semantic analysis on the variable declaration
    """
    var_data_type = self.declaration_stack[0]["name"] # Data type of the variable

    # If value is declared when the variable is initialize, perform type checking
    if (len(self.declaration_stack) == 4):
      value = self.declaration_stack[3]

      if (var_data_type == "INT"): # If the variable is an integer, check if the value is an integer
        if (value["name"] == "IDENT"):
          variable_type = self.symbol_table.get_symbol(value["value"])["type"]
          
          if (variable_type != "INT"): # If the value is not an integer, append an error message
            self.errors.append(f'Semantic Error in line {self.declaration_line}: {value["value"]} is {variable_type} (Expected {var_data_type})')
      
    # Operations is detected
    if(len(self.declaration_stack) > 4): # If the variable is initialized with an expression, perform semantic analysis on the expression
      self.operation_stack = self.declaration_stack[3::]
      resulting_type = self._expressionSemanticAnalysis()
      
      if (var_data_type != resulting_type): # If the resulting type of the expression does not match the variable type, append an error message
        self.errors.append(f"Semantic Error in line {self.declaration_line}: The resulting type of expression '{' '.join(list(map(lambda x: x['name'] if x['value'] == None else x['value'], self.operation_stack)))}' is {resulting_type}. (Expected {var_data_type})")
        
      self._resetOperationStates() # Reset the operation states


  def _assignmentSemanticAnalysis(self):
    """
      Perform semantic analysis on the assignment statement
    """
    variable = self.assignment_stack[1] # Get the variable from the assignment stack
    variable_type = self.symbol_table.get_symbol(variable["value"])["type"] # Get the type of the variable
    value = self.assignment_stack[3] # Get the value from the assignment stack

    # Check if value is a variable
    if (value["name"] == "IDENT"):
      var = self.symbol_table.get_symbol(value["value"])
      var_type = var["type"]

      if (variable_type == "INT" and var_type == "STR"): # If the variable is an integer and the value is a string, append an error message
        self.errors.append(f"Semantic Error in line {self.in_assignment_line}: {value["value"]} is {var_type}. (Expected {variable_type})")
        
    # Check if value is an expression
    elif (value["name"] in self.arithmetic_operators):
      self.operation_stack = self.assignment_stack[3::]
      resulting_type = self._expressionSemanticAnalysis() 
      
      if (variable_type == "INT" and resulting_type == "STR"): # If the variable is an integer and the resulting type of the expression is a string, append an error message
        self.errors.append(f"Semantic Error in line {self.in_assignment_line}: The resulting type of expression '{' '.join(list(map(lambda x: x['name'] if x['value'] == None else x['value'], self.operation_stack)))}' is {resulting_type}. (Exptected {variable_type})")
      
      self._resetOperationStates()
    
  def _resetVarDeclStates(self):
    """
      Reset the variable declaration states
    """
    self.in_declaration = False
    self.declaration_stack = []
    self.declaration_line = 0
  
  def _resetAssignState(self):
    """
      Reset the assignment states
    """
    self.in_assignment = False
    self.assignment_stack = []
    self.assignment_stack_index = 0
    self.in_assignment_line = 0
  
  def _resetOperationStates(self):
    """
      Reset the operation states
    """
    self.operation_stack = []
    self.operation_stack_index = 0

  def parse(self, input_tokens: list[dict]):
    """
      Parse the input tokens using the production and parse tables.
    """
    # Reset the containers
    self.total_output = []
    self.input_buffer = []
    self.errors = []
    self.is_valid = True

    self.stack.append('$') # End symbol
    self.stack.append(self.prod_table[0][1]) # Start symbol is the first symbol of the first production
    current_symbol = self.stack.pop() # Get the current symbol from the stack

    # Iterate through each line of the input tokens.
    for line in input_tokens:
      self.line_number = line

      # Stop the function if an error is found
      if not self.is_valid:
        break

      # Add the line to the input buffer
      for token in input_tokens[line]:
        self.input_buffer.append(token)
      
      # Initialize the current input and symbol
      current_input = self.input_buffer[0]

      # Iterate through the stack and input buffer until the stack is empty or the end of the input is reached
      while (current_symbol != '$' and len(self.stack) != 0 and len(self.input_buffer) != 0):
        
        # If the current symbol matches the current input
        if (current_symbol == current_input["name"]):
          if (current_symbol == "LOI"): 
            if (self.in_assignment): # If the parser is in assignment, perform semantic analysis
              self._assignmentSemanticAnalysis()
              self._resetAssignState()
              
            elif (self.in_declaration): # If the parser is in declaration, perform semantic analysis
              self._varDeclarationSemanticAnalysis()
              self._resetVarDeclStates()

          if (self.in_declaration): # If the parser is in declaration, append the input to the declaration stack
            self.declaration_stack.append(current_input)
          
          if (self.in_assignment): # If the parser is in assignment, append the input to the assignment stack
            self.assignment_stack.append(current_input)

          self.input_buffer.pop(0) # Remove the first element of the input buffer
          
          # Update the current symbol and input
          current_symbol = self.stack.pop()
          current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else ''

        # if there is token mismatch, append error message
        elif (current_symbol.isupper() and current_symbol != current_input["name"]):
          self.errors.append(f'Error on line {line} | Terminal mismatch - Expected {current_symbol}, found {current_input["name"]} with value {current_input["value"]}')
          self.is_valid = False
          break

        # if the current symbol is non-terminal, get the production from the parse table
        else:
          parse_row = self._getParseTableRow(current_symbol)
          parse_col = self._getParseTableCol(current_input["name"])

          # If the parse_row or col is not a valid index raise error
          if parse_row == None or parse_col == None:
            self.errors.append(f'Error on line {line} | No production found for input {current_input["name"]} with value {current_input["value"]}')
            self.is_valid = False
            break

          parse_cell = self.parse_table[parse_row][parse_col]

          # if the parse cell is empty raise error 
          if parse_cell == '':
            self.errors.append(f'Error on line {line} | No production found for input {current_input["name"]} with value {current_input["value"]}')
            self.is_valid = False
            break
          
          # Get the production from the production table
          production = self.prod_table[int(parse_cell) - 1][2]
          production_name = self.prod_table[int(parse_cell) - 1][1]
          production_symbols = production.strip().split(' ')

          if(production_name == "VariableDeclaration"): # If the production is a variable declaration
            self.in_assignment = False

            if (self.in_declaration): # If the parser is in declaration, perform semantic analysis
              self._varDeclarationSemanticAnalysis()
              self._resetVarDeclStates
            
            self.in_declaration = True # Set the parser to declaration
            self.declaration_line = line # Set the declaration line
            
          if (self.in_declaration and production_name == "VarDeclTail"): # If the parser is in declaration and the production is a variable declaration tail
            if ('e' in production_symbols): # If the production contains epsilon, perform semantic analysis
              self._varDeclarationSemanticAnalysis()
              self._resetVarDeclStates

          if(production_name == "Assignment"): # If the production is an assignment
            self.in_declaration = False

            if(self.in_assignment): # If the parser is in assignment, perform semantic analysis
              self._assignmentSemanticAnalysis()
              self._resetAssignState()
            
            self.in_assignment = True
            self.in_assignment_line = line
          
          if(production_name in ["Input", "Output"]): # If the production is an input or output
            if (self.in_assignment):
              self._assignmentSemanticAnalysis()
              self._resetAssignState()

            elif (self.in_declaration):
              self._varDeclarationSemanticAnalysis()
              self._resetVarDeclStates()
            
          # Add the symbols to stack in reverse order
          for symbol in production_symbols[::-1]:
            if symbol != 'e':
              self.stack.append(symbol)
          
          current_symbol = self.stack.pop()


