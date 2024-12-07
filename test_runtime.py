import tkinter as tk 
from symbol_table import SymbolTable

class Runtime:
  def __init__(self, console_text_widget):
    self.console_text_widget = console_text_widget
    self.symbol_table = SymbolTable()
    self.tokens = {}

    self.line_number = 1
    self.token_index = 0

    self.arithmetic_operators = ["ADD", "SUB", "MULT", "DIV"]

  def _get_next_token(self):
    commands = self.tokens[self.line_number]

    if self.token_index >= len(commands):
      self.line_number += 1
      self.token_index = 0
      return self._get_next_token()

    # Update the token index
    self.token_index += 1
    return commands[self.token_index - 1]
    
  def _process_arithmetic_operator(self, current_operator: str):
    # Get the first operand
    op1 = self._get_next_token()

    # If the operand is a variable, get its value from the symbol table
    if op1["name"] == "IDENT":
      op1_type = self.symbol_table.get_symbol(op1["value"])["type"]
      # if type is not int, raise an error
      if op1_type != "INT":
        raise Exception(f"Error: Operand {op1['value']} is not an integer")
      op1_value = int(self.symbol_table.get_symbol(op1["value"])["value"])

    # If the operand is an integer literal, get its value
    elif op1["name"] == "INT_LIT":
      op1_value = int(op1["value"])

    # if the operand is an arithmetic operator, get the result of the operation
    elif op1["name"] in self.arithmetic_operators:
      result = self._process_arithmetic_operator(op1["name"])
      op1_value = result
    
    # Get the second operand
    op2 = self._get_next_token()

    # If the operand is a variable, get its value from the symbol table
    if op2["name"] == "IDENT":
      op2_type = self.symbol_table.get_symbol(op2["value"])["type"]
      # if type is not int, raise an error
      if op2_type != "INT":
        raise Exception(f"Error: Operand {op2['value']} is not an integer")
      op2_value = int(self.symbol_table.get_symbol(op2["value"])["value"])

    # If the operand is an integer literal, get its value
    elif op2["name"] == "INT_LIT":
      op2_value = int(op2["value"])

    # if the operand is an arithmetic operator, get the result of the operation
    elif op2["name"] in self.arithmetic_operators:
      result = self._process_arithmetic_operator(op2["name"])
      op2_value = result

    # Perform the operation
    if current_operator == "ADD":
      return op1_value + op2_value
    elif current_operator == "SUB":
      return op1_value - op2_value
    elif current_operator == "MULT":
      return op1_value * op2_value
    elif current_operator == "DIV":
      if op2_value == 0:
        if op2["name"] == "IDENT":
          raise Exception(f"Error at line {self.line_number}: Division by zero in variable {op2['value']}")
        else:
          raise Exception(f"Error at line {self.line_number}: Division by zero in integer literal {op2['value']}")
      return op1_value / op2_value

  def process_input_code(self, tokens: dict, symbol_table: SymbolTable):
    self.symbol_table = symbol_table
    self.tokens = tokens

    self.line_number = 1
    self.token_index = 0

    current_token = self._get_next_token()

    while current_token["name"] != "LOI":
      if current_token["name"] in self.arithmetic_operators:
        result = self._process_arithmetic_operator(current_token["name"])
        print(result)

      current_token = self._get_next_token()

