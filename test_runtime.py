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

  def get_next_token(self):
    commands = self.tokens[self.line_number]

    if self.token_index >= len(commands):
      self.line_number += 1
      self.token_index = 0
      return self.get_next_token()

    # Update the token index
    self.token_index += 1
    return commands[self.token_index - 1]
    
  def process_arithmetic_operator(self, operator: str, op1: dict, op2: dict):
    if op1["name"] == "IDENT":
      op1_value = self.symbol_table.get_symbol(op1["value"])["value"]
      op1_type = self.symbol_table.get_symbol(op1["value"])["type"]
    else:
      op1_value = op1["value"]
      op1_type = "INT" if op1["name"] == "INTLIT" else "STR"

    if op2["name"] == "IDENT":
      op2_value = self.symbol_table.get_symbol(op2["value"])["value"]
      op2_type = self.symbol_table.get_symbol(op2["value"])["type"]
    else:
      op2_value = op2["value"]
      op2_type = "INT" if op2["name"] == "INTLIT" else "STR"

    # Semantic analysis for the arithmetic operator
    if op1_type == "STR" or op2_type == "STR":
      raise Exception("Error: Arithmetic operation between string and integer")

    # Perform the arithmetic operation
    if operator == "ADD":
      return op1_value + op2_value
    elif operator == "SUB":
      return op1_value - op2_value
    elif operator == "MULT":
      return op1_value * op2_value
    elif operator == "DIV":
      if op2_value == 0:
        raise Exception("Error: Division by zero")
      return op1_value / op2_value

  def process_input_code(self, tokens: dict, symbol_table: SymbolTable):
    self.symbol_table = symbol_table
    self.tokens = tokens

    self.line_number = 1
    self.token_index = 0

    current_token = self.get_next_token()

    while current_token["name"] != "LOI":
      if current_token["name"] in self.arithmetic_operators:
        current_operator = current_token["name"]
        op1 = self.get_next_token()
        op2 = self.get_next_token()

        result = self.process_arithmetic_operator(current_operator, op1, op2)
        print(result)
      
      current_token = self.get_next_token()

