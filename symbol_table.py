class SymbolTable:
  def __init__(self):
    self.symbol_table = {}
  
  def add_symbol(self, symbol: str, type: str, value: str | int):
    self.symbol_table[symbol] = {"type": type, "value": value}
  
  def get_symbol(self, symbol: str):
    return self.symbol_table[symbol]

  def remove_all_symbols(self):
    self.symbol_table = {}
  
  def get_symbol_table(self):
    return self.symbol_table