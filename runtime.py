import re
import tkinter as tk 
from symbol_table import SymbolTable

class Runtime:
  """
    Runtime class for running the input code 
  """
  def __init__(self, console_text_widget):
    # Initialize the console text widget, symbol table, tokens, line number, and token index
    self.console_text_widget = console_text_widget
    self.symbol_table = SymbolTable()
    self.tokens = {}

    self.line_number = 1
    self.token_index = 0
    
    self.errors = []

    self.arithmetic_operators = ["ADD", "SUB", "MULT", "DIV", "MOD"]

  def _get_next_token(self):
    """
      Gets the next token from the tokens dictionary.
    """
    commands = self.tokens[self.line_number] # Get the commands in the current line

    if self.token_index >= len(commands): # If the token index is greater than the length of the commands, move to the next line
      self.line_number += 1
      self.token_index = 0
      return self._get_next_token()

    # Update the token index
    self.token_index += 1
    return commands[self.token_index - 1]

  def _peek_next_token(self):
    """
      Peeks the next token from the tokens dictionary.
    """
    commands = self.tokens[self.line_number]
    return commands[self.token_index]
  
  def _process_arithmetic_operator(self, current_operator: str):
    """
      Processes the arithmetic operator in the input code.
    """
    op1 = self._get_next_token() # Get first operand

    # If the operand is a variable, get its value from the symbol table
    if op1["name"] == "IDENT":
      op1_type = self.symbol_table.get_symbol(op1["value"])["type"]
      
      if op1_type != "INT": # if type is not int, raise an error
        self.errors.append(f"Runtime error on line {self.line_number} | Operand {op1['value']} is not an integer")
        raise Exception(f"Error: Operand {op1['value']} is not an integer")
      
      op1_value = int(self.symbol_table.get_symbol(op1["value"])["value"]) # Get the value of the variable
 
    elif op1["name"] == "INT_LIT": # Get the value of the integer literal
      op1_value = int(op1["value"])

    elif op1["name"] in self.arithmetic_operators: # Get the result of the operation
      result = self._process_arithmetic_operator(op1["name"])
      op1_value = result
    
    op2 = self._get_next_token() # Get the second operand

    if op2["name"] == "IDENT": # Get the value of the variable
      op2_type = self.symbol_table.get_symbol(op2["value"])["type"]
      
      if op2_type != "INT": # if type is not int, raise an error
        self.errors.append(f"Runtime error on line {self.line_number} | Operand {op2['value']} is not an integer")
        raise Exception(f"Error | Operand {op2['value']} is not an integer")
      
      op2_value = int(self.symbol_table.get_symbol(op2["value"])["value"]) # Get the value of the variable

    elif op2["name"] == "INT_LIT": # Get the value of the integer literal
      op2_value = int(op2["value"])

    elif op2["name"] in self.arithmetic_operators: # Get the result of the operation
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
      if op2_value == 0: # If division by zero, raise an error
        if op2["name"] == "IDENT":
          self.errors.append(f"Runtime error on line {self.line_number} | Division by zero in variable {op2['value']}")
          raise Exception(f"Runtime error on line {self.line_number} | Division by zero in variable {op2['value']}")
        else:
          self. error_message.append(f"Runtime error on line {self.line_number} | Division by zero in integer literal {op2['value']}")
          raise Exception(f"Runtime error on line {self.line_number} | Division by zero in integer literal {op2['value']}")
      return op1_value / op2_value
    
  def _process_print(self):
    """
      Processes the print operation in the input code.
    """
    token_to_print = self._get_next_token() # Get the token to print

    # If the token to print is a variable, get its value from the symbol table
    if token_to_print["name"] == "IDENT":
      value = self.symbol_table.get_symbol(token_to_print["value"])["value"]
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, value)
      self.console_text_widget.see(tk.END)
      self.console_text_widget.config(state=tk.DISABLED)
    
    # If the token to print is an integer literal, insert it into the console text widget
    elif token_to_print["name"] == "INT_LIT":
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, token_to_print["value"])
      self.console_text_widget.see(tk.END)
      self.console_text_widget.config(state=tk.DISABLED)
    
    # If the token to print is an arithmetic operator, get the result of the operation and insert it into the console text widget
    elif token_to_print["name"] in self.arithmetic_operators:
      result = self._process_arithmetic_operator(token_to_print["name"])
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, result)
      self.console_text_widget.see(tk.END)
      self.console_text_widget.config(state=tk.DISABLED)
  
  def process_input_code(self, tokens: dict, symbol_table: SymbolTable):
    """
      Iterates through the tokens and processes them.
    """
    self.symbol_table = symbol_table
    self.tokens = tokens

    self.line_number = 1
    self.token_index = 0

    current_token = self._get_next_token()

    # Iterate through the tokens until the end of the input code
    while current_token["name"] != "LOI": 
      
      if self.errors: # If any error message is encountered, stop the runtime
        break
      
      if current_token["name"] in self.arithmetic_operators: # If the token is an arithmetic operator, process it
        result = self._process_arithmetic_operator(current_token["name"])

      elif current_token["name"] == "PRINT": # If the token is a print operation, process it
        self._process_print()

      elif current_token["name"] == "NEWLN": # If the token is a newline, insert a newline into the console text widget
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, "\n")
        self.console_text_widget.see(tk.END)
        self.console_text_widget.config(state=tk.DISABLED)
      
      elif current_token["name"] == "INTO": # If the token is an INTO operation, process it
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
            ident_type = self.symbol_table.get_symbol(value["value"])["type"]
            if ident_type == "STR":
                self.errors.append(f"Error: Cannot store f{ident_type} type into variable f{variable['name']}")
                raise Exception(f"Error: Cannot store f{ident_type} type into variable f{variable["name"]}")
            self.symbol_table.update_symbol(variable["value"], int(ident_value))
        
      # Input operation in the form BEG var_name  
      elif current_token["name"] == "BEG":
        variable = self._get_next_token()
        variable_type = self.symbol_table.get_symbol(variable["value"])["type"]
        
        # if the variable is not in the symbol table, raise an error
        if not self.symbol_table.get_symbol(variable["value"]):
          self.errors.append(f"Runtime error on line {self.line_number} | Variable {variable['value']} is not declared")
          break
          # raise Exception(f"Runtime error on line {self.line_number} | Variable {variable['value']} is not declared")
        
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, "Input for " + variable["value"] + ": ")
        self.console_text_widget.config(state=tk.DISABLED) 
               
        # Get user input
        user_input = tk.simpledialog.askstring("Input", f"Enter value for {variable['value']} (type: {variable_type})")
        
        # If cancel button is clicked, treat it as an empty input
        if user_input == None:
          user_input = ""
          
        # Check data type of user input and match with variable type
        if variable_type == "INT":  
          if not re.fullmatch(r'^[0-9]+$', user_input):
            self.errors.append(f"Runtime error on line {self.line_number} | Expected an integer for variable {variable['value']}")
            break
         
          if user_input == "":  # If the user input is empty, raise error
            self.errors.append(f"Runtime error on line {self.line_number} | Empty input for variable {variable['value']}")
            break
            
          self.symbol_table.update_symbol(variable["value"], int(user_input)) # Update variable value if the user input is valid
          
          # Update console text widget
          self.console_text_widget.config(state=tk.NORMAL)
          self.console_text_widget.insert(tk.END, user_input + "\n") 
          self.console_text_widget.see(tk.END)
          self.console_text_widget.config(state=tk.DISABLED)
            
        elif variable_type == "STR": # STR input
          # Validate that the input is not a pure number
          if re.fullmatch(r'^[0-9]+$', user_input):
            self.errors.append(f"Runtime error on line {self.line_number} | Expected a string for variable {variable['value']}")
            break
          
          self.symbol_table.update_symbol(variable["value"], user_input)
          
          self.console_text_widget.config(state=tk.NORMAL)
          self.console_text_widget.insert(tk.END, user_input + "\n")
          self.console_text_widget.see(tk.END)
          self.console_text_widget.config(state=tk.DISABLED)
      

      current_token = self._get_next_token()
    
    # If no error message, update the console text widget
    # If there is any error message, update the console and stop runtime
    if self.errors:
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, "\n\nProgram terminated due to encountered error:\n")
      for error in self.errors:
        self.console_text_widget.insert(tk.END, error + "\n")
      self.console_text_widget.see(tk.END)
      self.console_text_widget.config(state=tk.DISABLED)
      
    else:
      self.console_text_widget.config(state=tk.NORMAL)
      self.console_text_widget.insert(tk.END, "\n\nProgram terminated successfully...")
      self.console_text_widget.see(tk.END)
      self.console_text_widget.config(state=tk.DISABLED)
      