# CMSC 129 Programming Project 
# Simple Compiler for Integer-Oriented Language (IOL)

# Authors:
# - DUYAG, Charmagne Jane
# - PADERNA, Rafael
# - VILLAMOR, John Noel

# Last Modified: 12/08/2024

# Libraries
import tkinter as tk # Tkinter for GUI
from tkinter import ttk, Menu, filedialog, messagebox

from lexical_analyzer import LexicalAnalyzer # Lexical Analysis component
from parser import Parser # Syntax Analysis and Static Semantics component

from symbol_table import SymbolTable # Symbol Table component
from runtime import Runtime

class CompilerApp:
  """
  Main class to represent the IDE.
  """
  def __init__(self):
    # Initialize variables
    self.is_dark_mode = True
    self.variables = []
    self.current_input = ""
    self.tokenized_output = ""
    self.file_directory = ""
    self.current_display_input = True
    self.opened_file = False
    self.error_message = []
    
    # Initialize classes
    self.symbol_table = SymbolTable()
    self.lexical_analyzer = LexicalAnalyzer()
    self.parser = Parser(self.symbol_table)
    
    # Set up the main window
    self.main_window = tk.Tk()
    self.main_window.title("CMSC 129 - Integer-Oriented Language IDE")
    self.main_window.geometry("900x600")
    
    # Set initial theme to dark mode
    self.bg_color = "#2c2c2c"
    self.text_color = "#ffffff"
    self.button_color = "#0082C8"
    self.frame_color = "#3a3a3a"
    
    # Header Frame
    self.header_frame = tk.Frame(self.main_window, bg=self.bg_color)
    self.header_frame.pack(fill="x", pady=5)
    
    # Header Label
    self.header_label = tk.Label(self.header_frame, text="Integer-Oriented Language IDE", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
    self.header_label.pack(side="left", padx=20)

    # Menu bar
    self.menu = Menu(self.main_window)

    # File Menu
    self.file_menu = Menu(self.menu, tearoff=0)
    self.file_menu.add_command(label="New File", command=self.new_file, accelerator="Ctrl+N")
    self.file_menu.add_command(label="Open File", command=self.open_file, accelerator="Ctrl+O")
    self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
    self.file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
    self.menu.add_cascade(label="File", menu=self.file_menu)

    # Compile Menu
    self.compile_menu = Menu(self.menu, tearoff=0)
    self.compile_menu.add_command(label="Compile Code", command=self.compile_code, accelerator="Ctrl+C")
    self.compile_menu.add_command(label="Show Tokenized Code", command=self.show_tokenized_output, accelerator="Ctrl+J")
    self.menu.add_cascade(label="Compile", menu=self.compile_menu)

    # Run Menu
    self.run_menu = Menu(self.menu, tearoff=0)
    self.run_menu.add_command(label="Execute Code", command=self.execute_code, accelerator="Ctrl+E")
    self.menu.add_cascade(label="Run", menu=self.run_menu)
    
    self.main_window.config(menu=self.menu)

    # Bind keyboard shortcuts
    self.main_window.bind("<Control-n>", lambda event: self.new_file())
    self.main_window.bind("<Control-o>", lambda event: self.open_file())
    self.main_window.bind("<Control-s>", lambda event: self.save_file())
    self.main_window.bind("<Control-S>", lambda event: self.save_file_as())
    self.main_window.bind("<Control-c>", lambda event: self.compile_code())
    self.main_window.bind("<Control-j>", lambda event: self.show_tokenized_output())
    self.main_window.bind("<Control-e>", lambda event: self.execute_code())

    # Frame for source code area
    self.code_frame_wrapper = tk.Frame(self.main_window, bg=self.bg_color)
    self.code_frame_wrapper.place(relx=0.03, rely=0.1, relwidth=0.65, relheight=0.65)
    
    # Tab label of source code area
    self.tab_label = "Untitled.iol"
    self.code_frame_label = tk.Label(self.code_frame_wrapper, text=self.tab_label, font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color, anchor="w")
    self.code_frame_label.pack(side="top", fill="x", pady=(0, 2))  # Slight padding for separation

    # Source code textarea
    self.code_frame = tk.Frame(self.code_frame_wrapper, bg=self.bg_color, bd=0)
    self.code_frame.pack(fill="both", expand=True)
    self.code_text = tk.Text(self.code_frame, font=("Consolas", 12), bg=self.frame_color, fg=self.text_color, wrap="word", padx=10, pady=10, relief="flat", insertbackground=self.text_color)
    self.code_text.pack(fill="both", expand=True)
    
    # Output area
    self.console_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0, relief="flat")
    self.console_frame.place(relx=0.03, rely=0.78, relwidth=0.94, relheight=0.18)

    # Create a text widget for output with scrollbars
    self.console_text = tk.Text(self.console_frame, font=("Consolas", 12), bg=self.frame_color, fg=self.text_color, wrap="word", padx=10, pady=10)
    self.console_text.insert(tk.END, "Awaiting action...")
    self.console_text.pack(side="left", fill="both", expand=True)
    self.console_text.config(state=tk.DISABLED)

    # Variable tables wrapper
    self.variables_frame_wrapper = tk.Frame(self.main_window, bg=self.bg_color)
    self.variables_frame_wrapper.place(relx=0.7, rely=0.1, relwidth=0.27, relheight=0.65)
    
    # Header for the variables table
    self.variables_header = tk.Label(self.variables_frame_wrapper, text="Variables", font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color)
    self.variables_header.pack(side="top", fill="x", pady=(0, 2))

    # Frame for the treeview (table)
    self.variables_frame = tk.Frame(self.variables_frame_wrapper, bg=self.bg_color, bd=0)
    self.variables_frame.pack(fill="both", expand=True)

    # Treeview for the variables
    self.tree = ttk.Treeview(self.variables_frame, columns=("Variable", "Type"), show="headings")
    self.tree.heading("Variable", text="Variable")
    self.tree.heading("Type", text="Type")
    self.tree.column("Variable", anchor="center", width=80)
    self.tree.column("Type", anchor="center", width=80)
    self.tree.pack(fill="both", expand=True)

    # Initialize Runtime after code_text and console_text are created
    self.runtime = Runtime(self.console_text)
  
  # Function to update the console text
  def update_console_text(self, text: str, operation: str = "insert"):
    if operation == "insert": # Append text
      self.console_text.config(state=tk.NORMAL) # Enable text editing
      self.console_text.insert(tk.END, text) # Insert text
      self.console_text.see(tk.END) # Scroll to the end
      self.console_text.config(state=tk.DISABLED) # Disable text editing
      
    else: # Overwrite text
      self.console_text.config(state=tk.NORMAL)
      self.console_text.delete(1.0, tk.END) # Reset text for overwriting
      self.console_text.insert(tk.END, text)
      self.console_text.see(tk.END)
      self.console_text.config(state=tk.DISABLED)
      
  # Function to run the main application
  def run(self):
    self.apply_dark_mode() # Dark mode theme
    self.main_window.mainloop() # Run the main application
  
  # Function to apply theme changes
  def apply_dark_mode(self):
    self.main_window.config(bg=self.bg_color)
    self.code_frame.config(bg=self.bg_color)
    self.code_text.config(bg=self.frame_color, fg=self.text_color, insertbackground=self.text_color)
    self.console_frame.config(bg=self.bg_color)
    self.console_text.config(bg=self.frame_color, fg=self.text_color)
    self.variables_frame.config(bg=self.bg_color)

    # Treeview widget colors
    self.style = ttk.Style()
    self.style.configure("Treeview", background=self.frame_color, foreground=self.text_color, fieldbackground=self.frame_color)
    self.style.map("Treeview", background=[('selected', self.button_color)], foreground=[('selected', 'white')])

  # Function to handle new file creation
  def new_file(self):
    self.code_frame_label.config(text="Untitled")
    self.code_text.delete(1.0, tk.END)
    self.reset_console_and_variables()
    self.console_text.delete(1.0, tk.END)
    self.update_console_text("New file created. Awaiting action...", "overwrite")
    
  # Function to open a file and load its content
  def open_file(self):
    file_path = filedialog.askopenfilename(filetypes=[("Input files", "*.iol")])
    if file_path:
      self.file_directory = file_path.split("/")
      self.file_directory = "/".join(self.file_directory[:-1])
      
      with open(file_path, 'r') as file:
        code_content = file.read()
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code_content)
        self.main_window.title(f"Syntax Analyzer - {file_path.split('/')[-1]}")
    
      # Update tab label
      self.tab_label = file_path.split("/")[-1]
      self.code_frame_label.config(text=self.tab_label)
      self.opened_file = True
      
      self.update_console_text(f"Input {self.tab_label} file loaded successfully.", "overwrite")
  
  # Function to save the current code to a file
  def save_file(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
      with open(file_path, 'w') as file:
        file.write(self.code_text.get(1.0, tk.END))
      
      if not self.opened_file:
        # Update tab label if it's a new file
        self.tab_label = file_path.split("/")[-1]
        self.code_frame_label.config(text=self.tab_label)
        self.update_console_text(f"File saved as {file_path.split('/')[-1]}.", "overwrite")
        
      else:
        self.opened_file = False
        self.update_console_text(f"File saved successfully.", "overwrite")
      

  # Function to save the current code to a file without changing the name
  def save_file_as(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
      with open(file_path, 'w') as file:
        file.write(self.code_text.get(1.0, tk.END))
        self.main_window.title(f"Syntax Analyzer - {file_path.split('/')[-1]}")
        
      # Update tab label
      self.tab_label = file_path.split("/")[-1]
      self.code_frame_label.config(text=self.tab_label)
      self.opened_file = True
      
      self.update_console_text(f"File saved as {file_path.split('/')[-1]}.", "overwrite")

  # Function to perform lexical analysis (tokenization) on the code
  def perform_lexical_analysis(self):
    self.reset_console_and_variables()
    self.symbol_table.remove_all_symbols()
    self.lexical_analyzer.variables.clear()

    code = self.code_text.get(1.0, tk.END).strip()
    self.current_input = code
    
    if not code: # Empty code textarea
      self.update_console_text("Lexical Analysis failed. No code to analyze.", "overwrite")
      return False
    
    start_code = code.split("\n")[0].strip().split(' ')[0]
    end_code = code.split("\n")[-1].strip().split(' ')[-1] 
    
    if start_code != "IOL" or end_code != "LOI":
      self.update_console_text("Lexical Analysis failed. Please ensure that the code starts with IOL and ends with LOI.", "overwrite")
      return False
    
    self.lexical_analyzer.tokenizeInput(code)

    for variable in self.lexical_analyzer.variables:
      self.symbol_table.add_symbol(
        variable["name"],
        variable["data_type"],
        variable["value"]
      )
    
    variables = self.symbol_table.get_symbol_table()
    self.show_variables(variables)

    lexical_output = self.lexical_analyzer.getOutput()
    
    # Tokenize the output 
    for token in lexical_output:
      for item in lexical_output[token]:
         self.tokenized_output += f"{item['name']} "
      self.tokenized_output += "\n"
    
    # Check for errors in lexical analysis
    if self.lexical_analyzer.errors:
      for error in self.lexical_analyzer.errors:
        self.error_message.append(error)
      
    # Write tokenized output to a file
    with open(f"{self.file_directory}/output.tkn", "w") as file:
      file.write(self.tokenized_output)
  
  # Function to perform syntax analysis on the tokenized code
  def perform_syntax_analysis(self):
    tokens = self.lexical_analyzer.getOutput() # Get the tokenized code
    
    self.parser.parse(tokens) # Parse the tokenized code
    
    for error in self.parser.errors:
      self.error_message.append(error)
    
  def compile_code(self):
    self.tokenized_output = ""
    self.current_input = self.code_text.get(1.0, tk.END).strip()
    
    if not self.current_display_input: # If the code has been modified, update the current input
        return
    
    self.symbol_table.remove_all_symbols()
    self.perform_lexical_analysis()  # Perform lexical analysis
    
    self.perform_syntax_analysis() # Perform syntax analysis
    
    # Guard clause for any errors in lexical, syntax, and static semantics
    if self.error_message:
      self.update_console_text(f"Compilation completed with errors:\n\n", "overwrite")
     
      for error in self.error_message: # Display errors
        self.update_console_text(f"{error}\n", "insert")
      
      return # Do not proceed to execution if there are errors
    
    # If no errors, proceed to execution
    self.update_console_text("Code compiled with no errors found. Program will now be executed...", "overwrite")
    self.execute_code()
    
  def execute_code(self):
    # Check if the code has been compiled
    tokens = self.lexical_analyzer.getOutput()
    
    # Get the current code
    code = self.code_text.get(1.0, tk.END).strip()
    self.current_input = code
    
    if not code: # Empty code textarea
      self.update_console_text("Execution failed. No code to execute.", "overwrite")
      return
    
    # If tokens is empty, the code has not been compiled
    if not tokens:
        self.update_console_text("Execution failed. Please compile the code first.\n", "overwrite")
        return
    
    
    # Execute the code if there are no errors
    self.update_console_text("\n\n=== IOL Execution ===\n", "insert")
    self.runtime.process_input_code(tokens, self.symbol_table)

  # Function to perform tokenization based on regex patterns
  def show_tokenized_output(self): 
      # Get current text from code display area
      current_text = self.code_text.get(1.0, tk.END).strip()
      
      # If text has been modified or not compiled yet
      if current_text != self.current_input or not self.tokenized_output:
          self.update_console_text("Please compile the code first.\n", "overwrite")
          return
          
      # Create tokenized output window
      token_window = tk.Toplevel()
      token_window.title("Tokenized Code")
      token_window.geometry("600x400")
      
      # Configure window to match main theme
      token_window.configure(bg=self.bg_color)
      
      # Create text widget for tokenized output
      token_text = tk.Text(
          token_window, 
          wrap=tk.WORD,
          font=("Consolas", 12),
          bg=self.frame_color,
          fg=self.text_color,
          padx=10,
          pady=10
      )
      token_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
      
      # Insert tokenized output
      token_text.insert(tk.END, self.tokenized_output)
      
      # Make text read-only
      token_text.config(state=tk.DISABLED)

  # Function to display variables in the symbol table
  def show_variables(self, variable_list):
    # Clear existing rows in the treeview
    for item in self.tree.get_children():
        self.tree.delete(item)
        
    # Insert variables into the treeview widget
    for variable in variable_list:
        # Access the 'type' and 'value' from the dictionary
        var_type = variable_list[variable]['type']
        var_value = variable_list[variable]['value'] if variable_list[variable]['value'] else ''
        
        # If type is error, go to the next variable
        if var_type == "ERROR":
            continue
        
        # Insert values into the treeview
        self.tree.insert('', 'end', values=(variable, var_type, var_value))

  # Function used to reset the console and variables
  def reset_console_and_variables(self):
    self.current_input = "" # Reset current input
    self.variables = [] # Reset variables
    self.symbol_table.remove_all_symbols() # Clear symbol table
    self.show_variables(self.symbol_table.get_symbol_table()) # Clear variables table
    self.console_text.insert(tk.END, "Awaiting action...") # Reset console text

# Main function to run the application
if __name__ == "__main__":
  app = CompilerApp()
  app.run()