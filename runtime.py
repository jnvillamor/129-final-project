import re
import tkinter as tk 
from symbol_table import SymbolTable

class Runtime:
  def __init__(self, console_text_widget):
    self.console_text_widget = console_text_widget
    self.symbol_table = SymbolTable()
    self.tokens = {}

    self.line_number = 1
    self.token_index = 0
    
    self.error_message = []

    self.arithmetic_operators = ["ADD", "SUB", "MULT", "DIV", "MOD"]

  def _get_next_token(self):
    commands = self.tokens[self.line_number]

    if self.token_index >= len(commands):
      self.line_number += 1
      self.token_index = 0
      return self._get_next_token()

    # Update the token index
    self.token_index += 1
    return commands[self.token_index - 1]

  def _peek_next_token(self):
    commands = self.tokens[self.line_number]
    return commands[self.token_index]
  
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
    
  def _process_print(self):
    token_to_print = self._get_next_token()

    # If the token to print is a variable, get its value from the symbol table
    if token_to_print["name"] == "IDENT":
      value = self.symbol_table.get_symbol(token_to_print["value"])["value"]
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, value)
      self.console_text_widget.config(state=tk.DISABLED)
    
    # If the token to print is an integer literal, insert it into the console text widget
    elif token_to_print["name"] == "INT_LIT":
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, token_to_print["value"])
      self.console_text_widget.config(state=tk.DISABLED)
    
    # If the token to print is an arithmetic operator, get the result of the operation and insert it into the console text widget
    elif token_to_print["name"] in self.arithmetic_operators:
      result = self._process_arithmetic_operator(token_to_print["name"])
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, result)
      self.console_text_widget.config(state=tk.DISABLED)
  
  # Iterate through the tokens and process them
  def process_input_code(self, tokens: dict, symbol_table: SymbolTable):
    self.symbol_table = symbol_table
    self.tokens = tokens

    self.line_number = 1
    self.token_index = 0

    current_token = self._get_next_token()

    while current_token["name"] != "LOI":
      if current_token["name"] in self.arithmetic_operators:
        result = self._process_arithmetic_operator(current_token["name"])

      elif current_token["name"] == "PRINT":
        self._process_print()

      elif current_token["name"] == "NEWLN":
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, "\n")
        self.console_text_widget.config(state=tk.DISABLED)
      
      elif current_token["name"] == "INTO":
        variable = self._get_next_token()
        is_keyword = self._get_next_token()
        value = self._get_next_token()

        if value["name"] == "INT_LIT":
          self.symbol_table.update_symbol(variable["value"], int(value["value"]))
        elif value["name"] == "IDENT":
          ident_value = self.symbol_table.get_symbol(value["value"])["value"]
          self.symbol_table.update_symbol(variable["value"], int(ident_value))
        elif value["name"] in self.arithmetic_operators:
          result = self._process_arithmetic_operator(value["name"])
          self.symbol_table.update_symbol(variable["value"], result)

      elif current_token["name"] == "INT":
        variable = self._get_next_token()

        if (self._peek_next_token()["name"] == "IS"):
          self._get_next_token()
          value = self._get_next_token()

          if value["name"] == "INT_LIT":
            self.symbol_table.update_symbol(variable["value"], int(value["value"]))
          elif value["name"] == "IDENT":
            ident_value = self.symbol_table.get_symbol(value["value"])["value"]
            self.symbol_table.update_symbol(variable["value"], int(ident_value))
        
      # Input operation in the form BEG var_name  
      elif current_token["name"] == "BEG":
        variable = self._get_next_token()
        variable_type = self.symbol_table.get_symbol(variable["value"])["type"]
        # print("variable", variable)
        
        # if the variable is not in the symbol table, raise an error
        if not self.symbol_table.get_symbol(variable["value"]):
          self.error_message.append(f"Error at line {self.line_number}: Variable {variable['value']} is not declared")
          break
          # raise Exception(f"Error at line {self.line_number}: Variable {variable['value']} is not declared")
        
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, "Input for " + variable["value"] + ": ")
        self.console_text_widget.config(state=tk.DISABLED) 
               
        # Get user input
        user_input = tk.simpledialog.askstring("Input", f"Enter value for {variable['value']} (type: {variable_type})")
        
        # Check data type of user input and match with variable type
        if variable_type == "INT":  
          if not re.fullmatch(r'^[0-9]+$', user_input):
            self.error_message.append(f"Error at line {self.line_number}: Expected an integer for variable {variable['value']}")
            break
         
          if user_input == "" or None:  # If the user input is empty, raise error
            self.error_message.append(f"Error at line {self.line_number}: Empty input for variable {variable['value']}")
            break
            
          self.symbol_table.update_symbol(variable["value"], int(user_input)) # Update variable value if the user input is valid
          print("Updated variable", variable["value"], "to", user_input)
          
          # Update console text widget
          self.console_text_widget.config(state=tk.NORMAL)
          self.console_text_widget.insert(tk.END, user_input + "\n") 
          self.console_text_widget.config(state=tk.DISABLED)
            
        elif variable_type == "STR": # STR input
          # Validate that the input is not a pure number
          if re.fullmatch(r'^[0-9]+$', user_input):
            self.error_message.append(f"Error at line {self.line_number}: Expected a string for variable {variable['value']}")
            break
          
          self.symbol_table.update_symbol(variable["value"], user_input)
          print("Updated variable", variable["value"], "to", user_input)
          
          self.console_text_widget.config(state=tk.NORMAL)
          self.console_text_widget.insert(tk.END, user_input + "\n")
          self.console_text_widget.config(state=tk.DISABLED)
      
      # If there is any error message, update the console and stop runtime
      if self.error_message:
        self.console_text_widget.config(state=tk.NORMAL)
        for error in self.error_message:
          self.console_text_widget.insert(tk.END, error + "\n")
          
        self.console_text_widget.insert(tk.END, "\nProgram terminated due to errors...")
        self.console_text_widget.config(state=tk.DISABLED)
        
        break 
      
      current_token = self._get_next_token()
    
    self.console_text_widget.config(state=tk.NORMAL)
    self.console_text_widget.insert(tk.END, "\n\nProgram terminated successfully...")
    self.console_text_widget.config(state=tk.DISABLED)

