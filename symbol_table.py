class SymbolTable:
  """ 
    Class to represent the symbol table.
    Stores the symbol, type and value of the symbol.
    In this program, this class stores variables encountered in the input code.
  """
  def __init__(self):
    self.symbol_table = {}
  
  def add_symbol(self, symbol: str, type: str, value: str | int):
    self.symbol_table[symbol] = {"type": type, "value": value}
  
  def get_symbol(self, symbol: str):
    return self.symbol_table[symbol]

  def remove_all_symbols(self):
    self.symbol_table.clear()
  
  def get_symbol_table(self):
    return self.symbol_table
  
  def update_symbol(self, symbol: str, value: str | int):
    self.symbol_table[symbol]["value"] = value
  
  # Print the symbol table
  def print_symbol_table(self):
    for symbol in self.symbol_table:
      print(f"{symbol}: {self.symbol_table[symbol]}")
