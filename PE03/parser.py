# Note: If the result of parsing is VALID, the output file should contain the complete solution of the parsing. 
# If the result of parsing is INVALID, the output file should contain the partial solution of the parsing to the point where parsing can no longer proceed. 
# (invalid) Then add another line stating an error (under the Action column).

# Has three columns:
# 1. Stack: The current stack of the parser
# 2. Input Buffer: The current input buffer
# 3. Action: The action taken by the parser

# Parser starts here

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
    self.file_path = str

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
              self.tokens.add(symbol) if symbol.islower() or symbol in ['+', '-', '*', '/', '%'] else None
            self.prod_table.append(line.strip().split(','))
        
      except:
        print('Error: File not found')
        return("Error - file not found")

    if input_file.endswith('.ptbl'):
      try:
        with open(input_file, "r", encoding="UTF-8") as file:
          lines = file.readlines()
          for line in lines:
            self.parse_table.append(line.strip().split(','))
        
      except:
        print(f'Error: {input_file} not found')
        return("Error - file not found")
      
    # If invalid input file, return error message
    if not (input_file.endswith('.prod') or input_file.endswith('.ptbl')):
      print('Error: Input file is not a .prod or .ptbl file')
      return("Error - invalid input file")
  
    # Return input status message
    print("LOADED: " + input_file)
    return("Loaded: " + input_file)
  
  def is_valid_input(self, input: str) -> bool: 
    # Check if input is valid
    for symbol in input.strip().split(' '):
      if symbol not in self.tokens:
        return False
    return True

  '''
  get_parse_row(symbol: str) -> int
  This function returns the row of the parse table corresponding to the given symbol.
  '''
  def get_parse_row(self, symbol: str):
    for ind, X in enumerate(self.parse_table):
      if X[0] == symbol:
        return ind
  
  '''
  get_parse_col(symbol: str) -> int
  This function returns the column of the parse table corresponding to the given symbol.
  '''
  def get_parse_col(self, symbol: str):
    for ind, X in enumerate(self.parse_table[0]):
      if X == symbol:
        return ind

  '''
  parse(input_string: str)
  This function parses the input string using the production and parse tables.
  '''
  def parse(self, input_string: str):
    # Check if input is valid
    if not self.is_valid_input(input_string):
      print('Error: Invalid input')
      return("Error - invalid input")

    # Initialize the input buffer and stack
    self.input_buffer = input_string.strip().split(' ')
    self.stack.append('$')
    self.stack.append(self.prod_table[0][1])
    
    # Add to the total output the initial
    self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', ''])
    # Get the current symbol and input
    current_symbol = self.stack.pop()
    current_input = self.input_buffer[0]
  
    # Parse the input string 
    while (current_symbol != '$' and len(self.stack) != 0):
      # If the symbol and input match, pop the stack and input buffer
      if(current_symbol == current_input):
        self.action.append(f'Match {current_symbol}')
        self.input_buffer.pop(0)
        self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
        
        current_symbol = self.stack.pop()
        current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else '$'
        

      # If the symbol is a terminal and does not match the input, add an error
      elif(current_symbol.islower() and current_symbol != current_input):
        self.action.append('Error')
        break
      
      elif(current_symbol.isupper()):
        # Get the production from the parse table
        parse_row = self.get_parse_row(current_symbol)
        parse_col = self.get_parse_col(current_input)
        parse_cell = self.parse_table[parse_row][parse_col]
        if parse_cell == '':
          self.action.append('Error')
          break

        production = self.prod_table[int(parse_cell) - 1][2]

        for symbol in production.strip().split(' ')[::-1]:
          self.stack.append(symbol) if symbol != 'e' else None
        self.action.append(f'Output {current_symbol} > {production}')
        self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
        current_symbol = self.stack.pop()

    # If the stack is empty, the input is valid
    if len(self.stack) == 0:
      self.is_valid = True
      self.action.append('Match $')
      self.total_output.append(['', '', self.action[-1]])
    else:
      self.is_valid = False

    for line in self.total_output:
      print(line)


  def exportOutput(self, output_file_name = "output"):
    file = open(f'{self.file_path}/{output_file_name}.prsd', "w")
    for line in self.total_output:
      file.write(','.join(line) + '\n')
    pass
