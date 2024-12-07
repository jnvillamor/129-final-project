"""
Class for parsing the input string using user-input production and parse tables.
"""

from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable

class Parser:
  def __init__(self, symbol_table: SymbolTable):
    self.prod_table = []
    self.parse_table = []
    self.symbol_table = symbol_table

    self.stack = []
    self.input_buffer = []
    self.action = []
    self.total_output = []

    self.is_valid = bool
    self.error_message = []

    # Flags for variable semantic checks
    self.is_variable_declaration = False
    self.current_data_type = None
    self.current_identifier = None
    self.is_waiting_for_value = False

    # Flags for assignment semantic checks
    self.is_assignment = False

    self._getProdTable()
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
  
  def _handleVariableDeclaration(self, current_input: dict, current_symbol: str, line: int):
    """
      Handle semantic checks for variable declarations in the parsing process.
      
      This function manages the state of variable declarations by tracking:
      - Whether we're currently processing a variable declaration
      - The current data type being declared (INT or STR)
      - The identifier being declared
      - Whether we're waiting for a value assignment
      
      It performs type checking to ensure:
      - Variables are declared with valid data types (INT or STR)
      - Assigned values match the declared type
      - When assigning from another variable, types are compatible
      
      Args:
          current_input (dict): Dictionary containing the current token information
          current_symbol (str): The current symbol being processed
          line (int): The current line number in the source code
          
      Side Effects:
          - Updates internal state flags for declaration processing
          - Adds error messages to self.error_message for type mismatches
          - Updates symbol table entries via self.symbol_table
    """
    if current_symbol in ["INT", "STR"]:
      print("Variable Declaration Flag Set")
      self.is_variable_declaration = True
      self.current_data_type = current_symbol

    elif self.is_variable_declaration and not self.is_waiting_for_value and current_symbol == "IDENT":
      print("Identifier Set")
      self.current_identifier = current_input["value"]

    elif self.is_variable_declaration and not self.is_waiting_for_value and current_symbol == "IS":
      # Keep the flag on, waiting for value
      self.is_waiting_for_value = True
      print("Waiting for value")

    elif self.is_variable_declaration and self.is_waiting_for_value:
      # Check value type matches declaration
      if current_symbol == "INT_LIT":
        if self.current_data_type != "INT": # If the declared type is not INT, throw an error
          self.error_message.append(f'Error at line {line}: Type mismatch - Variable {self.current_identifier} declared as {self.current_data_type} but assigned {current_input["value"]}')

      elif current_symbol == "IDENT":
        # Check if the identifier has the same data type as the declaration
        if self.symbol_table.get_symbol(current_input["value"])["type"] != self.current_data_type:
          self.error_message.append(f'Error at line {line}: Type mismatch - Variable {self.current_identifier} declared as {self.current_data_type} but assigned {self.symbol_table.get_symbol(current_input["value"])["type"]}')
      
      # Reset flags after processing the declaration
      print("Resetting flags")
      self.is_variable_declaration = False
      self.is_waiting_for_value = False
      self.current_data_type = None
      self.current_identifier = None
    
    else:
      # If we're not waiting for a value, reset the flags
      self.is_variable_declaration = False
      self.is_waiting_for_value = False
      self.current_data_type = None
      self.current_identifier = None

  def _handleAssignment(self, current_input: dict, current_symbol: str, line: int):
    """
    Handle semantic checks for assignment statements (INTO identifier IS expression).
    Ensures type compatibility between the identifier and the assigned expression.
    
    Args:
        current_input (dict): Dictionary containing the current token information
        current_symbol (str): The current symbol being processed
        line (int): The current line number in the source code
        
    Side Effects:

    """
    # If the current symbol is INTO, set the flag and reset the current identifier and waiting for value flag
    if current_symbol == "INTO":
      self.is_assignment = True
      self.current_identifier = None
      self.is_waiting_for_value = False
    
    # If the current symbol is an identifier and we haven't set the current identifier yet, store it
    elif current_symbol == "IDENT" and self.current_identifier is None:
      # Store the identifier being assigned to
      self.current_identifier = current_input["value"]
      # Get its type from symbol table
      self.current_data_type = self.symbol_table.get_symbol(current_input["value"])["type"]
    
    # If we're waiting for a value, set the flag
    elif current_symbol == "IS":
      self.is_waiting_for_value = True
    
    # If we're waiting for a value, check if it matches the declared type
    elif self.is_waiting_for_value:
      if current_symbol == "INT_LIT":
        if self.current_data_type != "INT": # If the declared type is not INT, throw an error
          self.error_message.append(f'Error at line {line}: Type mismatch in assignment - Variable {self.current_identifier} is {self.current_data_type} but assigned {current_input["value"]}')
      
      elif current_symbol == "IDENT": # If the identifier is not the same type as the declared type, throw an error
        if self.symbol_table.get_symbol(current_input["value"])["type"] != self.current_data_type:
          self.error_message.append(f'Error at line {line}: Type mismatch in assignment - Variable {self.current_identifier} is {self.current_data_type} but assigned {current_input["value"]}')
      
      # Reset flags
      self.is_assignment = False
      self.current_identifier = None
      self.current_data_type = None
      self.is_waiting_for_value = False
    
    # If we're not waiting for a value, reset the flags
    else:
      self.is_assignment = False
      self.current_identifier = None
      self.current_data_type = None
      self.is_waiting_for_value = False

  def _handleOperation(self, current_input: dict, current_symbol: str, line: int):
    """
    Handle semantic checks for arithmetic operations (ADD, MULT, SUB, DIV, MOD).
    Ensures both operands are of type INT.
    
    Args:
        current_input (dict): Dictionary containing the current token information
        current_symbol (str): The current symbol being processed
        line (int): The current line number in the source code
    
    Side Effects:
        - Adds error messages to self.error_message for type mismatches
    """
    if current_symbol in ["ADD", "MULT", "SUB", "DIV", "MOD"]:
        # Check first operand
        next_token = self.input_buffer[1] if len(self.input_buffer) > 1 else None
        second_token = self.input_buffer[2] if len(self.input_buffer) > 2 else None
        
        # Check if there are two operands to check types
        if next_token and second_token:
            # Check first operand
            if next_token["name"] == "IDENT":
                symbol_type = self.symbol_table.get_symbol(next_token["value"])["type"]
                if symbol_type != "INT":
                    self.error_message.append(f'Error at line {line} {current_symbol} {next_token["value"]} {second_token["value"]}: Type mismatch in operation - Expected INT but found {symbol_type} for operand {next_token["value"]}')
            elif next_token["name"] != "INT_LIT":
                  self.error_message.append(f'Error at line {line} {current_symbol} {next_token["value"]} {second_token["value"]}: Type mismatch in operation - Expected INT but found {symbol_type} for operand {next_token["value"]}')
            
            # Check second operand
            if second_token["name"] == "IDENT":
                symbol_type = self.symbol_table.get_symbol(second_token["value"])["type"]
                if symbol_type != "INT":
                  self.error_message.append(f'Error at line {line} {current_symbol} {next_token["value"]} {second_token["value"]}: Type mismatch in operation - Expected INT but found {symbol_type} for operand {second_token["value"]}')
            elif second_token["name"] != "INT_LIT":
              self.error_message.append(f'Error at line {line} {current_symbol} {next_token["value"]} {second_token["value"]}: Type mismatch in operation - Expected INT but found {symbol_type} for operand {second_token["value"]}')

  def parse(self, input_tokens: list[dict]):
    """
      Parse the input tokens using the production and parse tables.
      
      Side Effects:
        - Adds error messages to self.error_message for type mismatches
        - Updates self.is_valid to False if an error is encountered
    """
    self.total_output = []
    self.input_buffer = []
    self.error_message = []
    self.is_valid = True
    self.stack.append('$')
    self.stack.append(self.prod_table[0][1])
    current_symbol = self.stack.pop()
    
    # Iterate through each line of the input tokens
    for line in input_tokens:
      if not self.is_valid: # If an error is encountered, break out of the loop
        break
      
      # Add the line to the input buffer
      for token in input_tokens[line]:
        self.input_buffer.append(token)

      # Initialize current input and symbol
      current_input = self.input_buffer[0]
      
      # Iterate through the stack and input buffer until the stack is empty or the end of the input is reached
      while (current_symbol != '$' and len(self.stack) != 0 and len(self.input_buffer) != 0):
        print(f"\nCurrent Symbol: {current_symbol} | Current Input: {current_input}")

        # If the current symbol matches the current input, perform semantic checks
        if(current_symbol == current_input["name"]):
          # Add semantic checks for variable declarations and assignments
          if self.is_variable_declaration or current_symbol in ["INT", "STR"]:
            print("Running semantic checks for variable declaration")
            self._handleVariableDeclaration(current_input, current_symbol, line)
            
          elif self.is_assignment or current_symbol == "INTO":
            print("Running semantic checks for assignment")
            self._handleAssignment(current_input, current_symbol, line)
            
          # If the current symbol is an arithmetic operation, perform semantic checks
          if current_symbol in ["ADD", "MULT", "SUB", "DIV", "MOD"]:
            print("Running semantic checks for operation")
            # self._handleOperation(current_input, current_symbol, line)

          # If the current symbol matches the current input, pop the input buffer and update the current symbol
          print("Match")
          self.input_buffer.pop(0)
          current_symbol = self.stack.pop()
          current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else ''
        
        # If the current symbol is a terminal and does not match the current input, throw an error
        elif(current_symbol.isupper() and current_symbol != current_input["name"]):
          print(f'Error at line {line}: Terminal mismatch - Expected {current_symbol}, found {current_input["name"]} with value {current_input["value"]}')
          self.is_valid = False
          break
        
        # If the current symbol is not a terminal, get the production from the parse table
        else:
          print("Getting production")
          # Get the production from the parse table
          parse_row = self._getParseTableRow(current_symbol)
          parse_col = self._getParseTableCol(current_input["name"])
          parse_cell = self.parse_table[parse_row][parse_col]

          # If the production is empty, throw an error  
          if parse_cell == '':
            self.error_message.append(f'Error at line {line}: No production found for input {current_input["name"]} with value {current_input["value"]}')
            print(f'Error at line {line}: No production found for input {current_input["name"]} with value {current_input["value"]}')
            self.is_valid = False
            break

          # Get the production from the production table
          production = self.prod_table[int(parse_cell) - 1][2]
          production_symbols = production.strip().split(' ')

          # Add symbols to stack in reverse order
          for symbol in production_symbols[::-1]:
            if symbol != 'e': # If the symbol is not epsilon, add it to the stack
              self.stack.append(symbol)
            else: # If the symbol is epsilon, reset flags
              print("e production")
              # If DataType IDENT is completed, reset flags
              if self.is_variable_declaration and self.current_identifier is not None:
                self.is_variable_declaration = False
                self.current_identifier = None
                self.is_waiting_for_value = False
                self.current_data_type = None

          # Print the production  
          print(f'Output {current_symbol} > {production}')
          # Update the current symbol
          current_symbol = self.stack.pop()

    # Print the errors if any
    if len(self.error_message) != 0:
      for error in self.error_message:
        print(error)
