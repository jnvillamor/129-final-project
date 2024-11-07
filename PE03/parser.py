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
   
    self.stack = []
    self.input_buffer = []
    self.action = []
    self.total_output = []
    
    self.is_valid = bool

  def getInput(self, input_file: str):
    if input_file.endswith('.prod'):
      try:
        with open(input_file, "r", encoding="UTF-8") as file:
          lines = file.readlines()
          for line in lines:
            self.prod_table.append(line.strip().split(','))
        
      except:
        print('Error: File not found')
        return("Error - file not found")

      print("PROD: " + self.prod_table)

    if input_file.endswith('.ptbl'):
      try:
        with open(input_file, "r", encoding="UTF-8") as file:
          lines = file.readlines()
          for line in lines:
            self.parse_table.append(line.strip().split(','))
        
      except:
        print(f'Error: {input_file} not found')
        return("Error - file not found")
      
      print("PTBL: " + self.parse_table)
      
    # If invalid input file, return error message
    if not (input_file.endswith('.prod') or input_file.endswith('.ptbl')):
      print('Error: Input file is not a .prod or .ptbl file')
      return("Error - invalid input file")
  
    # Return input status message
    print("LOADED: " + input_file)
    return("Loaded: " + input_file)
   
  def parse(self, input_string):
    
    pass
  
  def exportOutput(self):
    # Append to total_output 
    
    # Export to .prsd file
    
    pass