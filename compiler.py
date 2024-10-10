from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable

class Compiler:
  def __init__(self):
    self.lexical_analyzer = LexicalAnalyzer()
    self.tokenize_code = ""
    self.symbol_table = SymbolTable()
  
  def compile(self, code: str):
    """ Compile the source code """

    # Check if the code is valid
    if code == "":
      print("Error: No code to compile")
      return
    
    # Compile the code
    code = code.strip() 
    split_code = code.split('\n')

    if (not split_code[0].strip().split()[0] == 'IOL'):
      raise Exception("Error: Invalid code")
    
    if (not split_code[-1].strip().split()[-1] == 'LOI'):
      raise Exception("Error: Invalid code")
    
    # Remove the IOL and LOI
    split_code[0] = split_code[0].replace('IOL', '')
    split_code[-1] = split_code[-1].replace('LOI', '')

    final_input = "\n".join(split_code)
    self.lexical_analyzer.tokenizeInput(final_input)
    
    # Append variables to the symbol table
    for variable in self.lexical_analyzer.variables:
      self.symbol_table.add_symbol(variable.get("name"), variable.get("data_type"), variable.get("value"))
