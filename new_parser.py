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

    self.is_variable_declaration = False
    self.current_data_type = None
    self.current_identifier = None
    self.is_waiting_for_value = False

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
  
  def parse(self, input_tokens: list[dict]):
    """
      Parse the input tokens using the production and parse tables.
    """
    self.total_output = []
    self.input_buffer = []
    self.stack.append('$')
    self.stack.append(self.prod_table[0][1])
    current_symbol = self.stack.pop()
    
    for line in input_tokens:
      # Add the line to the input buffer
      for token in input_tokens[line]:
        self.input_buffer.append(token)

      current_input = self.input_buffer[0]
      while (current_symbol != '$' and len(self.stack) != 0 and len(self.input_buffer) != 0):
        print(f"\nCurrent Symbol: {current_symbol} | Current Input: {current_input}")

        if(current_symbol == current_input["name"]):
          # Add semantic checks for variable declarations
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
            if current_symbol in ["INT_LIT", "STR_LIT"]:
              expected_type = "INT_LIT" if self.current_data_type == "INT" else "STR_LIT"
              if current_symbol != expected_type:
                self.error_message.append(f'Error at line {line}: Type mismatch - Variable {self.current_identifier} declared as {self.current_data_type} but assigned {self.symbol_table.get_symbol(current_input["value"])["type"]}')
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

          print("Match")
          self.input_buffer.pop(0)
          current_symbol = self.stack.pop()
          current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else ''
        
        elif(current_symbol.isupper() and current_symbol != current_input["name"]):
          print(f'Error at line {line}: Terminal mismatch - Expected {current_symbol}, found {current_input}')
          self.is_valid = False
          break

        else:
          print("Getting production")
          # Get the production from the parse table
          parse_row = self._getParseTableRow(current_symbol)
          parse_col = self._getParseTableCol(current_input["name"])
          parse_cell = self.parse_table[parse_row][parse_col]

          if parse_cell == '':
            print(f'Error at line {line}: No production found for input {current_input}')
            self.is_valid = False
            break

          production = self.prod_table[int(parse_cell) - 1][2]
          production_symbols = production.strip().split(' ')

          # Add symbols to stack in reverse order
          for symbol in production_symbols[::-1]:
            if symbol != 'e':
              self.stack.append(symbol)

          print(f'Output {current_symbol} > {production}')
          current_symbol = self.stack.pop()

    # Print the errors if any
    if len(self.error_message) != 0:
      for error in self.error_message:
        print(error)

if __name__ == "__main__":
  symbol_table = SymbolTable()
  lexical_analyzer = LexicalAnalyzer()
  lexical_analyzer.tokenizeInput("""
IOL
  INT num IS 0 INT res IS A
  STR msg1 STR msg2 STR msg3
  BEG msg1 BEG msg2
  BEG msg3
  NEWLN PRINT msg1
  NEWLN
  INTO res IS MULT num num
  PRINT msg2
  PRINT MULT num 2 
  NEWLN
  PRINT msg3
  PRINT res
LOI
""")
  
  variables = lexical_analyzer.getVariables()
  for variable in variables:
    symbol_table.add_symbol(variable["name"], variable["data_type"], variable["value"])

  parser = Parser(symbol_table)
  parser.parse(lexical_analyzer.getOutput())