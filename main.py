import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
from compiler import Compiler
from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable

class CompilerApp:
  def __init__(self):
    self.lexical_analyzer = LexicalAnalyzer()
    self.is_dark_mode = True
    self.variables = []
    self.current_input = ""
    self.compiler = Compiler()
    self.tokenized_output = ""
    self.symbol_table = SymbolTable()
    self.current_display_input = True

    # Set up the main window
    self.main_window = tk.Tk()
    self.main_window.title("LEXICAL ANALYZER")
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
    self.header_label = tk.Label(self.header_frame, text="Lexical Analyzer IDE", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
    self.header_label.pack(side="left", padx=20)

    # Toggle Button for Light/Dark mode
    self.toggle_button = tk.Button(self.header_frame, text="🌙" if self.is_dark_mode else "☀️", command=self.toggle_theme, bg=self.button_color, fg="white", font=("Arial", 12), relief="flat")
    self.toggle_button.pack(side="right", padx=20)

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
    self.compile_menu.add_command(label="Show Tokenized Code", command=self.compile_code, accelerator="Ctrl+T")
    self.menu.add_cascade(label="Compile", menu=self.compile_menu)

    # Run Menu
    self.run_menu = Menu(self.menu, tearoff=0)
    self.run_menu.add_command(label="Execute Code", command=self.execute_code, accelerator="Ctrl+E")
    self.menu.add_cascade(label="Run", menu=self.run_menu)

    self.main_window.config(menu=self.menu)

    # Bind keyboard shortcuts
    self.main_window.bind("<Control-n>", lambda event: self.clear_editor())
    self.main_window.bind("<Control-o>", lambda event: self.open_file())
    self.main_window.bind("<Control-s>", lambda event: self.save_file())
    self.main_window.bind("<Control-S>", lambda event: self.save_file_as())
    self.main_window.bind("<Control-c>", lambda event: self.compile_code())
    self.main_window.bind("<Control-t>", lambda event: self.compile_code())
    self.main_window.bind("<Control-e>", lambda event: self.execute_code())

    # Code display area
    self.code_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0)
    self.code_frame.place(relx=0.03, rely=0.1, relwidth=0.65, relheight=0.65)
    self.code_text = tk.Text(self.code_frame, font=("Consolas", 12), bg=self.frame_color, fg=self.text_color, wrap="word", padx=10, pady=10, relief="flat", insertbackground=self.text_color)
    self.code_text.pack(fill="both", expand=True)

    # Output area
    self.output_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0, relief="flat")
    self.output_frame.place(relx=0.03, rely=0.78, relwidth=0.65, relheight=0.18)
    self.output_label = tk.Label(self.output_frame, text="Output will be shown here.", font=("Consolas", 12), bg=self.frame_color, fg=self.text_color, anchor="nw", padx=10, pady=10)
    self.output_label.pack(fill="both", expand=True)

    # Variables table
    self.variables_frame = tk.Frame(self.main_window, bg=self.bg_color, bd=0)
    self.variables_frame.place(relx=0.7, rely=0.1, relwidth=0.27, relheight=0.65)
    self.tree = ttk.Treeview(self.variables_frame, columns=("Variable", "Type"), show="headings")
    self.tree.heading("Variable", text="Variable")
    self.tree.heading("Type", text="Type")
    # tree.heading("Value", text="Value")
    self.tree.column("Variable", anchor="center", width=80)
    self.tree.column("Type", anchor="center", width=80)
    # tree.column("Value", anchor="center", width=80)
    self.tree.pack(fill="both", expand=True)

    # Tokenized button
    self.button_container = tk.Frame(self.main_window, bg=self.bg_color, bd=0)
    self.button_container.place(relx=0.7, rely=0.78, relwidth=0.27, relheight=0.18)
    self.tokenized_button = self.generate_rounded_button(self.button_container, "Show Tokenized Output", self.show_tokenized_output)

  def run(self):
    self.apply_theme()
    self.main_window.mainloop()
  
  
  # Function to apply theme changes
  def apply_theme(self):
    self.main_window.config(bg=self.bg_color)
    self.header_frame.config(bg=self.bg_color)
    self.header_label.config(bg=self.bg_color, fg=self.text_color)
    self.code_frame.config(bg=self.bg_color)
    self.code_text.config(bg=self.frame_color, fg=self.text_color, insertbackground=self.text_color)
    self.output_frame.config(bg=self.bg_color)
    self.output_label.config(bg=self.frame_color, fg=self.text_color)
    self.variables_frame.config(bg=self.bg_color)
    self.button_container.config(bg=self.bg_color)

    # Treeview widget colors
    self.style = ttk.Style()
    self.style.configure("Treeview", background=self.frame_color, foreground=self.text_color, fieldbackground=self.frame_color)
    self.style.map("Treeview", background=[('selected', self.button_color)], foreground=[('selected', 'white')])

    # Button canvas background updates
    for widget in self.button_container.winfo_children():
      if isinstance(widget, tk.Canvas):
        widget.config(bg=self.bg_color)

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
    file_path = filedialog.askopenfilename(filetypes=[("Input files", "*.iol"), ("All files", "*.*")])
    if file_path:
      with open(file_path, 'r') as file:
        code_content = file.read()
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code_content)
        self.main_window.title(f"LEXICAL ANALYZER - {file_path.split('/')[-1]}")
  
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
        self.main_window.title(f"LEXICAL ANALYZER - {file_path.split('/')[-1]}")

  # Function for Lexical Analysis (tokenization)
  def compile_code(self):
    if(not self.current_display_input): return
    self.output_label.config(text="Performing Lexical Analysis...")
    code = self.code_text.get(1.0, tk.END).strip() # Get the code from the editor
    
    # Check if code is empty
    if not code:
        messagebox.showwarning("Alert", "Please input or load code for analysis.")
        self.output_label.config(text="Lexical Analysis failed. No code to analyze.")
        return
    
    try:        
        # Compile the code
        self.reset_output_and_tree()
        code = code.strip()
        self.current_input = code
        split_code = code.split('\n')

        if (not split_code[0].strip().split()[0] == 'IOL'):
            raise Exception("Error: Invalid code")
        
        if (not split_code[-1].strip().split()[-1] == 'LOI'):
            raise Exception("Error: Invalid code")
        
        final_input = "\n".join(split_code)
        self.lexical_analyzer.tokenizeInput(final_input)
    
        # Append variables to the symbol table
        for variable in self.lexical_analyzer.variables:
         self.symbol_table.add_symbol(variable.get("name"), variable.get("data_type"), variable.get("value"))

        # tokens = tokenize_input(code)
        variables = self.symbol_table.get_symbol_table()
        self.display_variables(variables)
        self.tokenized_output = self.lexical_analyzer.output
        self.output_label.config(text="Lexical Analysis successful. No errors found.")
    except Exception as e:
        self.output_label.config(text=f"Lexical Analysis failed. {str(e)}")
        return

  # Function to perform tokenization based on regex patterns
  def show_tokenized_output(self):
    if(self.current_display_input):
        if self.tokenized_output != "": 
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, self.tokenized_output)
            self.current_display_input = not self.current_display_input
    else:
        print()
        if self.current_input != "":
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, self.current_input)
            self.current_display_input = not self.current_display_input
    

  # Function to display variables in the symbol table
  def display_variables(self, variable_list):
    self.reset_output_and_tree()
    
    # Insert variables into the treeview widget
    for variable in variable_list:
        # Access the 'type' and 'value' from the dictionary
        var_type = variable_list[variable]['type']
        var_value = variable_list[variable]['value'] if variable_list[variable]['value'] else ''
        
        # Insert values into the treeview
        self.tree.insert('', 'end', values=(variable, var_type, var_value))

  # Function for syntax analysis (dummy implementation for now)
  def analyze_syntax(self):
    self.output_label.config(text="Syntax analysis successful. No errors found.")

  # Function to execute the code (placeholder for now)
  def execute_code(self):
    self.output_label.config(text="Executing code... (Output will be shown here)")

  # Function to clear the editor
  def clear_editor(self):
    self.code_text.delete(1.0, tk.END)
    self.reset_output_and_tree()

  # Function to reset the output label and variable table
  def reset_output_and_tree(self):
    self.variables = []
    self.symbol_table.remove_all_symbols()
    self.output_label.config(text="Output will be shown here.")
    for item in self.tree.get_children():
      self.tree.delete(item)

if __name__ == "__main__":
  app = CompilerApp()
  app.run()