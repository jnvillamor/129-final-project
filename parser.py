'''
Class for parsing the input string using user-input production and parse tables.
'''
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
  def parse(self, input_string: str):
    self.total_output = []
    # Read the input file and save its content
    try:
      with open(input_string, "r", encoding="UTF-8") as file:
        input = file.read().strip().split('\n')
    except:
      print(f'Error: {input_string} not found')
      return("Error - file not found")

    for line in input[1:-1]:
      # Initialize the input buffer and stack
      self.input_buffer = line.strip().split(' ')
      self.input_buffer = ['IOL'] + self.input_buffer + ['LOI']
      self.stack.append('$')
      self.stack.append(self.prod_table[0][1])
      
      # Add to the total output the initial
      self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', ''])
      # Get the current symbol and input
      current_symbol = self.stack.pop()
      current_input = self.input_buffer[0]
    
      # Parse the input string 
      while (current_symbol != '$' and len(self.stack) != 0):
        print(self.total_output[-1])
        # If the symbol and input match, pop the stack and input buffer
        if(current_symbol == current_input):
          self.action.append(f'Match {current_symbol}')
          self.input_buffer.pop(0)
          self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
          
          current_symbol = self.stack.pop()
          current_input = self.input_buffer[0] if len(self.input_buffer) != 0 else '$'
          

        # If the symbol is a terminal and does not match the input, add an error
        elif(current_symbol.isupper() and current_symbol != current_input):
          self.action.append('Error: Terminal mismatch')
          self.error_message = 'Terminal mismatch'
          self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
          self.is_valid = False
          break
        
        elif(not current_symbol.isupper()):
          # Get the production from the parse table
          parse_row = self.getParseRow(current_symbol)
          parse_col = self.getParseCol(current_input)
          parse_cell = self.parse_table[parse_row][parse_col]
          if parse_cell == '':
            self.is_valid = False
            self.action.append('Error: No production found')
            self.error_message = 'No production found'
            self.total_output.append([' '.join(self.stack[::-1]), ' '.join(self.input_buffer) + '$', self.action[-1]])
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

if __name__ == "__main__":
  parser = Parser()
  parser.getInput('grammar.prod')
  parser.getInput('grammar.ptbl')
  parser.parse('output.tkn')
  parser.exportOutput('output1')
 