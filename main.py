# CMSC 129 PE04
# by DUYAG, PADERNA, VILLAMOR

import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable
from parser import Parser
from runtime import Runtime

class CompilerApp:
  """
  Main class to represent the IDE.
  """
  def __init__(self):
    self.is_dark_mode = True
    self.variables = []
    self.current_input = ""
    self.tokenized_output = ""
    self.file_directory = ""
    self.current_display_input = True
    
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
    self.file_menu.add_command(label="New File", command=self.clear_editor, accelerator="Ctrl+N")
    self.file_menu.add_command(label="Open File", command=self.open_file, accelerator="Ctrl+O")
    self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
    self.file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
    self.menu.add_cascade(label="File", menu=self.file_menu)

    # Compile Menu
    self.compile_menu = Menu(self.menu, tearoff=0)
    self.compile_menu.add_command(label="Compile Code", command=self.compile_code, accelerator="Ctrl+C")
    self.menu.add_cascade(label="Compile", menu=self.compile_menu)

    # Run Menu
    self.run_menu = Menu(self.menu, tearoff=0)
    self.run_menu.add_command(label="Execute Code", command=self.execute_code, accelerator="Ctrl+E")
    self.menu.add_cascade(label="Run", menu=self.run_menu)
    
    # View Menu
    self.view_menu = Menu(self.menu, tearoff=0)
    self.view_menu.add_command(label="Show Tokenized Code", command=self.show_tokenized_output, accelerator="Ctrl+J")
    self.view_menu.add_command(label="Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+D")
    self.menu.add_cascade(label="View", menu=self.view_menu)

    self.main_window.config(menu=self.menu)

    # Bind keyboard shortcuts
    self.main_window.bind("<Control-n>", lambda event: self.clear_editor())
    self.main_window.bind("<Control-o>", lambda event: self.open_file())
    self.main_window.bind("<Control-s>", lambda event: self.save_file())
    self.main_window.bind("<Control-S>", lambda event: self.save_file_as())
    self.main_window.bind("<Control-c>", lambda event: self.compile_code())
    self.main_window.bind("<Control-j>", lambda event: self.show_tokenized_output())
    self.main_window.bind("<Control-e>", lambda event: self.execute_code())
    self.main_window.bind("<Control-d>", lambda event: self.toggle_theme())

    # Code display area
    self.code_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0)
    self.code_frame.place(relx=0.03, rely=0.1, relwidth=0.65, relheight=0.65)
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

    # Variables table
    self.variables_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0)
    self.variables_frame.place(relx=0.7, rely=0.1, relwidth=0.27, relheight=0.65)
    self.tree = ttk.Treeview(self.variables_frame, columns=("Variable", "Type"), show="headings")
    self.tree.heading("Variable", text="Variable")
    self.tree.heading("Type", text="Type")
    self.tree.column("Variable", anchor="center", width=80)
    self.tree.column("Type", anchor="center", width=80)
    self.tree.pack(fill="both", expand=True)

    # Initialize Runtime after code_text and console_text are created
    self.runtime = Runtime(self.console_text)
  
  def update_console_text(self, text: str, operation: str = "insert"):
    # if the operation is insert, enable the text widget, append the text, and disable it again
    if operation == "insert":
      self.console_text.config(state=tk.NORMAL)
      self.console_text.insert(tk.END, text)
      self.console_text.config(state=tk.DISABLED)
    else:
      self.console_text.config(state=tk.NORMAL)
      self.console_text.delete(1.0, tk.END)
      self.console_text.insert(tk.END, text)
      self.console_text.config(state=tk.DISABLED)
      
  def run(self):
    self.apply_theme()
    
    # Run the main application
    self.main_window.mainloop()
  
  # Function to apply theme changes
  def apply_theme(self):
    self.main_window.config(bg=self.bg_color)
    self.code_frame.config(bg=self.bg_color)
    self.code_text.config(bg=self.frame_color, fg=self.text_color, insertbackground=self.text_color)
    self.console_frame.config(bg=self.bg_color)
    self.console_text.config(bg=self.frame_color, fg=self.text_color)
    self.variables_frame.config(bg=self.bg_color)
    # self.button_container.config(bg=self.bg_color)

    # Treeview widget colors
    self.style = ttk.Style()
    self.style.configure("Treeview", background=self.frame_color, foreground=self.text_color, fieldbackground=self.frame_color)
    self.style.map("Treeview", background=[('selected', self.button_color)], foreground=[('selected', 'white')])

  # Function to switch between dark mode and light mode
  def toggle_theme(self):
    self.is_dark_mode = not self.is_dark_mode
    if self.is_dark_mode:
      self.bg_color = "#2c2c2c"
      self.text_color = "#ffffff"
      self.button_color = "#0082C8"
      self.frame_color = "#3a3a3a"
    else:
      self.bg_color = "#f0f0f0"
      self.text_color = "#000000"
      self.button_color = "#007acc"
      self.frame_color = "#e0e0e0"

    # Apply theme changes
    self.apply_theme()

  # Function to generate a button with rounded corners
  def generate_rounded_button(self, parent, label, action):
    canvas = tk.Canvas(parent, width=200, height=40, bg=self.bg_color, highlightthickness=0)
    canvas.pack(pady=20)
    canvas.create_oval(0, 0, 40, 40, fill=self.button_color, outline=self.button_color)
    canvas.create_oval(160, 0, 200, 40, fill=self.button_color, outline=self.button_color)
    canvas.create_rectangle(20, 0, 180, 40, fill=self.button_color, outline=self.button_color)
    canvas.create_text(100, 20, text=label, fill=self.text_color, font=("Arial", 12))
    canvas.bind("<Button-1>", lambda event: action())
    return canvas

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
    
      self.update_console_text("Input .iol file loaded successfully.", "overwrite")
  
  # Function to save the current code to a file
  def save_file(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
      with open(file_path, 'w') as file:
        file.write(self.code_text.get(1.0, tk.END))

  # Function to save the current code to a file without changing the name
  def save_file_as(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
      with open(file_path, 'w') as file:
        file.write(self.code_text.get(1.0, tk.END))
        self.main_window.title(f"Syntax Analyzer - {file_path.split('/')[-1]}")

  # Function to perform lexical analysis (tokenization) on the code
  def perform_lexical_analysis(self):
    self.reset_output_and_tree()
    self.symbol_table.remove_all_symbols()
    self.lexical_analyzer.variables.clear()

    code = self.code_text.get(1.0, tk.END).strip()
    print(code)
    self.current_input = code
    
    self.update_console_text("Input .iol file loaded successfully.", "overwrite")
    if not code:
      messagebox.showwarning("Alert", "Please input or load code for analysis.")
      self.update_console_text("Lexical Analysis failed. No code to analyze.", "overwrite")
      return False
    
    start_code = code.split("\n")[0].strip().split(' ')[0]
    end_code = code.split("\n")[-1].strip().split(' ')[-1] 
    
    if start_code != "IOL" or end_code != "LOI":
      messagebox.showwarning("Alert", "Invalid code. Please ensure that the code starts with IOL and ends with LOI.")
      self.update_console_text("Lexical Analysis failed. Invalid code.", "overwrite")
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
    for token in lexical_output:
      for item in lexical_output[token]:
         self.tokenized_output += f"{item['name']} "
      self.tokenized_output += "\n"
    
    if self.lexical_analyzer.errors:
      error_message = "\n".join(self.lexical_analyzer.errors)
      self.update_console_text(f"Compilation completed. Lexical errors found:\n{error_message}", "overwrite")
      return False
    
    with open(f"{self.file_directory}/output.tkn", "w") as file:
      file.write(self.tokenized_output)
    
    # self.console_text.insert(tk.END, "Lexical Analysis completed successfully. \n")
    return True
  
  # Function to perform syntax analysis on the tokenized code
  def perform_syntax_analysis(self):
    # Parse the tokenized code
    self.parser.parse(self.lexical_analyzer.getOutput())
    
    if self.parser.is_valid:
      # self.console_text.insert(tk.END, "Syntax Analysis completed successfully. \n")
      return True
    else:
      self.update_console_text(f"Compilation completed. Syntax errors found:\n{self.parser.error_message}\n", "overwrite")
      
    if self.parser.error_message:
      error_message = "\n".join(self.parser.error_message)
      self.update_console_text(f"Compilation completed. Syntax errors found:\n{error_message}", "overwrite")
      return False
    
    
    return self.parser.is_valid
    
  # Function to perform semantic analysis on the tokenized code
  def perform_semantic_analysis(self):
   try:
       # Get the current code from the text widget
       code = self.code_text.get(1.0, tk.END).strip()
       
       # Perform semantic analysis
       self.semantic_analyzer.analyze_code(code)
       
       # If no errors, update the output label
       self.update_console_text("Semantic Analysis successful. No errors found.", "overwrite")
       return True
   except Exception as e:
       self.update_console_text(f"Semantic Analysis failed: {str(e)}", "overwrite")
       return False
    
  def compile_code(self):
    self.tokenized_output = ""
    self.current_input = self.code_text.get(1.0, tk.END).strip()
    
    if not self.current_display_input:
        return
    
    if not self.perform_lexical_analysis():
        return
    
    if not self.perform_syntax_analysis():
        return
    
    self.update_console_text("Code compiled with no errors found. Program will now be executed...\n", "overwrite")
    
  def execute_code(self):
    self.update_console_text("\n=== IOL Execution ===\n", "insert")
    # Check if the code has been compiled
    tokens = self.lexical_analyzer.getOutput()
    self.runtime.process_input_code(tokens, self.symbol_table)

  # Function to perform tokenization based on regex patterns
  def show_tokenized_output(self): 
      # Get current text from code display area
      current_text = self.code_text.get(1.0, tk.END).strip()
      
      # If text has been modified or not compiled yet
      if current_text != self.current_input or not self.tokenized_output:
          messagebox.showwarning("Alert", "Please compile the code first.")
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

  # Function to clear the editor
  def clear_editor(self):
    self.code_text.delete(1.0, tk.END)
    self.reset_output_and_tree()
    self.console_text.delete(1.0, tk.END)
    self.console_text.insert(tk.END, "Awaiting action...") # Reset the output label
    

  # Function to reset the output label and variable table
  def reset_output_and_tree(self):
    self.current_input = "" # Reset current input
    self.variables = [] # Reset variables
    self.symbol_table.remove_all_symbols() # Clear the symbol table
    self.show_variables(self.symbol_table.get_symbol_table()) # Clear the treeview widget
    self.console_text.insert(tk.END, "Awaiting action...") # Reset the output label

# Main function to run the application
    
if __name__ == "__main__":
  app = CompilerApp()
  app.run()