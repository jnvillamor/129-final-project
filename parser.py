'''
Class for parsing the input string using user-input production and parse tables.
'''
from parse_tree import ParseTree

class Parser:
  def __init__(self):
    self.prod_table = []
    self.parse_table = []
    self.tokens= set()

    self.stack = []
    self.input_buffer = []
    self.action = []
    self.total_output = []
    
    self.is_valid = bool
    self.error_message = str
    self.file_path = str

    self.parse_tree = None

  '''
  getInput(input_file: str) -> str[]
  This function reads the input file and stores the contents in the appropriate table.
  The function returns a status message indicating whether the input file was successfully loaded.
  '''
  def getInput(self, input_file: str):
    # Get the file path
    self.file_path = input_file.split('/')[:-1]
    self.file_path = '/'.join(self.file_path)

    if input_file.endswith('.prod'):
      try:
        with open(input_file, "r", encoding="UTF-8") as file:
          lines = file.readlines()
          for line in lines:
            prod_file = line.strip().split(',')
            prod_symbols = prod_file[2].strip().split(' ')
            for symbol in prod_symbols:
              self.tokens.add(symbol) if symbol.isupper() or symbol in ['+', '-', '*', '/', '%'] else None
            self.prod_table.append(line.strip().split(','))
        
        return ("prod", input_file.strip().split('/')[-1], self.prod_table)
        
      except:
        print('Error: File not found')
        return("Error - file not found")

    if input_file.endswith('.ptbl'):
      try:
        with open(input_file, "r", encoding="UTF-8") as file:
          lines = file.readlines()
          for line in lines:
            self.parse_table.append(line.strip().split(','))
            
        return ("ptbl", input_file.strip().split('/')[-1], self.parse_table)
        
      except:
        print(f'Error: {input_file} not found')
        return("Error - file not found")
      
    # If invalid input file, return error message
    if not (input_file.endswith('.prod') or input_file.endswith('.ptbl')):
      print('Error: Input file is not a .prod or .ptbl file')
      return("Error - invalid input file")

  '''
  getParseRow(symbol: str) -> int
  This function returns the row of the parse table corresponding to the given symbol.
  '''
  def getParseRow(self, symbol: str):
    for ind, X in enumerate(self.parse_table):
      if X[0] == symbol:
        return ind
  
  '''
  getParseCol(symbol: str) -> int
  This function returns the column of the parse table corresponding to the given symbol.
  '''
  def getParseCol(self, symbol: str):
    for ind, X in enumerate(self.parse_table[0]):
      if X == symbol:
        return ind

  '''
  parse(input_string: str)
  This function parses the input string using the production and parse tables.
  '''
  def parse(self, input_tokens: str):
    self.total_output = []
    self.parse_tree = ParseTree()

    # Split the input tokens into lines
    input_tokens = input_tokens.strip().split('\n')
    
    # Create a mapping of token positions to line numbers
    token_line_map = {}
    current_position = 0
    
    # Process each line to create token position mapping
    for line_num, line in enumerate(input_tokens, 1):
      tokens = line.strip().split()
      for token in tokens:
        token_line_map[current_position] = line_num
        current_position += 1

    input_tokens = ''.join(input_tokens)

    # Initialize the input buffer and stack
    self.input_buffer = input_tokens.strip().split(' ')
    self.stack.append('$')
    self.stack.append(self.prod_table[0][1])
    
    # Initialize the parse tree with the start symbol
    self.parse_tree.set_root(self.prod_table[0][1])
    
    # Add to the total output the initial
    self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', ''])
    # Get the current symbol and input
    current_symbol = self.stack.pop()
    current_input = self.input_buffer[0]
    current_token_position = 0
  
    # Parse the input string 
    while (current_symbol != '$' and len(self.stack) != 0):
      print(self.total_output[-1])
      # If the symbol and input match, pop the stack and input buffer
      if(current_symbol == current_input):
        self.parse_tree.add_node(current_symbol, "terminal")
        self.parse_tree.move_up()
        
        self.action.append(f'Match {current_symbol}')
        self.input_buffer.pop(0)
        current_token_position += 1
        self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
        
        current_symbol = self.stack.pop()
        current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else '$'

      # If the symbol is a terminal and does not match the input, add an error
      elif(current_symbol.isupper() and current_symbol != current_input):
        error_line = token_line_map.get(current_token_position, 'unknown')
        self.action.append(f'Error at line {error_line}: Terminal mismatch - Expected {current_symbol}, found {current_input}')
        self.error_message = f'Terminal mismatch at line {error_line}'
        self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
        self.is_valid = False
        break
      
      elif(not current_symbol.isupper()):
        # Get the production from the parse table
        parse_row = self.getParseRow(current_symbol)
        parse_col = self.getParseCol(current_input)
        parse_cell = self.parse_table[parse_row][parse_col]
        if parse_cell == '':
          error_line = token_line_map.get(current_token_position, 'unknown')
          self.action.append(f'Error at line {error_line}: No production found for input {current_input}')
          self.error_message = f'No production found at line {error_line}'
          self.is_valid = False
          self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
          break

        production = self.prod_table[int(parse_cell) - 1][2]
        production_symbols = production.strip().split(' ')

        # Add production to parse tree
        for symbol in production_symbols:
          if symbol != 'e':
            new_node = self.parse_tree.add_node(symbol, 
              "terminal" if symbol.isupper() or symbol in ['+', '-', '*', '/', '%'] 
              else "non-terminal")
        
        # Add symbols to stack in reverse order
        for symbol in production_symbols[::-1]:
          if symbol != 'e':
            self.stack.append(symbol)
        
        self.action.append(f'Output {current_symbol} > {production}')
        self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
        current_symbol = self.stack.pop()

    # If the stack is empty, the input is valid
    if len(self.stack) == 0:
      self.is_valid = True
      self.action.append('Match $')
      self.total_output.append(['', '', self.action[-1]])
    
    print(self.total_output[-1])

    return (self.is_valid, self.error_message, self.total_output)

  '''
  exportOutput(output_file_name: str) -> None
  This function exports the output to a .prsd file.
  '''
  def exportOutput(self, output_file_name = "output"):
    file = open(f'{self.file_path}/{output_file_name}.prsd', "w")
    for line in self.total_output:
      file.write(','.join(line) + '\n')
    pass

  def get_parse_tree(self):
    """Returns the parse tree if parsing was successful"""
    return self.parse_tree

if __name__ == "__main__":
  parser = Parser()
  parser.getInput('grammar.prod')
  parser.getInput('grammar.ptbl')
  input_token_file = 'output.tkn'
  with open(input_token_file, 'r') as file:
    input_tokens = file.read()
  parser.parse(input_tokens)
  if parser.is_valid:
    parse_tree = parser.get_parse_tree()
    parse_tree.print_tree()
  else:
    print(parser.error_message)