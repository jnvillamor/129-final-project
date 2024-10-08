import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
import re

# Global variable for theme mode
is_dark_mode = True

# Function to generate a button with rounded corners
def generate_rounded_button(parent, label, action):
    canvas = tk.Canvas(parent, width=200, height=40, bg=bg_color, highlightthickness=0)
    canvas.pack(pady=20)
    canvas.create_oval(0, 0, 40, 40, fill=button_color, outline=button_color)
    canvas.create_oval(160, 0, 200, 40, fill=button_color, outline=button_color)
    canvas.create_rectangle(20, 0, 180, 40, fill=button_color, outline=button_color)
    canvas.create_text(100, 20, text=label, fill=text_color, font=("Arial", 12))
    canvas.bind("<Button-1>", lambda event: action())
    return canvas

# Function to open a file and load its content
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Input files", "*.iol"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            code_content = file.read()
            code_text.delete(1.0, tk.END)
            code_text.insert(tk.END, code_content)
            main_window.title(f"LEXICAL ANALYZER - {file_path.split('/')[-1]}")

# Function to save the current code to a file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(code_text.get(1.0, tk.END))

# Function to save the current code to a file without changing the name
def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL Files", "*.iol")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(code_text.get(1.0, tk.END))
        main_window.title(f"LEXICAL ANALYZER - {file_path.split('/')[-1]}")

# Function for Lexical Analysis (tokenization)
def analyze_code():
    code = code_text.get(1.0, tk.END).strip()
    if not code:
        messagebox.showwarning("Alert", "Please input or load code for analysis.")
        return
    tokens = tokenize_code(code)
    display_tokens(tokens)

# Function to perform tokenization based on regex patterns
def tokenize_code(code):
    tokens = []
    patterns = {
        'NUMBER': r'\b\d+\b',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z_0-9]*',
        'KEYWORD': r'\b(INTO|BEG|PRINT|IS|IOL|LOI|INT|STR|ADD|SUB|MULT|DIV|MOD|NEWLN)\b',
        'OPERATOR': r'[+\-*/]',
        'DELIMITER': r'[();{}]',
        'WHITESPACE': r'\s+'
    }
    combined_regex = '|'.join(f'(?P<{key}>{value})' for key, value in patterns.items())
    for match in re.finditer(combined_regex, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type != 'WHITESPACE':
            tokens.append((token_value, token_type))
    return tokens

# Function to display tokens in the table
def display_tokens(tokens):
    reset_output_and_tree()
    for token_value, token_type in tokens:
        tree.insert('', 'end', values=(token_value, token_type, ''))

# Function for syntax analysis (dummy implementation for now)
def analyze_syntax():
    output_label.config(text="Syntax analysis successful. No errors found.")

# Function to execute the code (placeholder for now)
def execute_code():
    output_label.config(text="Executing code... (Output will be shown here)")

# Function to clear the editor
def clear_editor():
    code_text.delete(1.0, tk.END)
    reset_output_and_tree()

# Function to reset the output label and variable table
def reset_output_and_tree():
    output_label.config(text="Output will be shown here.")
    for item in tree.get_children():
        tree.delete(item)

# Function to switch between dark mode and light mode
def toggle_theme():
    global is_dark_mode, bg_color, text_color, button_color, frame_color
    is_dark_mode = not is_dark_mode
    if is_dark_mode:
        bg_color = "#2c2c2c"
        text_color = "#ffffff"
        button_color = "#0082C8"
        frame_color = "#3a3a3a"
    else:
        bg_color = "#f0f0f0"
        text_color = "#000000"
        button_color = "#007acc"
        frame_color = "#e0e0e0"

    # Apply theme changes
    apply_theme()

# Function to apply theme changes
def apply_theme():
    main_window.config(bg=bg_color)
    header_frame.config(bg=bg_color)
    header_label.config(bg=bg_color, fg=text_color)
    code_frame.config(bg=bg_color)
    code_text.config(bg=frame_color, fg=text_color, insertbackground=text_color)
    output_frame.config(bg=bg_color)
    output_label.config(bg=frame_color, fg=text_color)
    variables_frame.config(bg=bg_color)
    button_container.config(bg=bg_color)

    # Treeview widget colors
    style = ttk.Style()
    style.configure("Treeview", background=frame_color, foreground=text_color, fieldbackground=frame_color)
    style.map("Treeview", background=[('selected', button_color)], foreground=[('selected', 'white')])

    # Button canvas background updates
    for widget in button_container.winfo_children():
        widget.config(bg=bg_color)

# Set up the main window
main_window = tk.Tk()
main_window.title("LEXICAL ANALYZER")
main_window.geometry("900x600")

# Set initial theme to dark mode
bg_color = "#2c2c2c"
text_color = "#ffffff"
button_color = "#0082C8"
frame_color = "#3a3a3a"

# Header Frame
header_frame = tk.Frame(main_window, bg=bg_color)
header_frame.pack(fill="x", pady=5)

# Header Label
header_label = tk.Label(header_frame, text="Lexical Analyzer IDE", font=("Arial", 16, "bold"), bg=bg_color, fg=text_color)
header_label.pack(side="left", padx=20)

# Toggle Button for Light/Dark mode
toggle_button = tk.Button(header_frame, text="🌙" if is_dark_mode else "☀️", command=toggle_theme, bg=button_color, fg="white", font=("Arial", 12), relief="flat")
toggle_button.pack(side="right", padx=20)

# Menu bar
menu = Menu(main_window)

# File Menu
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="New File", command=clear_editor, accelerator="Ctrl+N")
file_menu.add_command(label="Open File", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_file_as, accelerator="Ctrl+Shift+S")
menu.add_cascade(label="File", menu=file_menu)

# Compile Menu
compile_menu = Menu(menu, tearoff=0)
compile_menu.add_command(label="Compile Code", command=analyze_code, accelerator="Ctrl+C")
compile_menu.add_command(label="Show Tokenized Code", command=analyze_code, accelerator="Ctrl+T")
menu.add_cascade(label="Compile", menu=compile_menu)

# Run Menu
run_menu = Menu(menu, tearoff=0)
run_menu.add_command(label="Execute Code", command=execute_code, accelerator="Ctrl+E")
menu.add_cascade(label="Run", menu=run_menu)

main_window.config(menu=menu)

# Bind keyboard shortcuts
main_window.bind("<Control-n>", lambda event: clear_editor())
main_window.bind("<Control-o>", lambda event: open_file())
main_window.bind("<Control-s>", lambda event: save_file())
main_window.bind("<Control-S>", lambda event: save_file_as())
main_window.bind("<Control-c>", lambda event: analyze_code())
main_window.bind("<Control-t>", lambda event: analyze_code())
main_window.bind("<Control-e>", lambda event: execute_code())

# Code display area
code_frame = tk.Frame(main_window, bg=bg_color, bd=0)
code_frame.place(relx=0.03, rely=0.1, relwidth=0.65, relheight=0.65)
code_text = tk.Text(code_frame, font=("Consolas", 12), bg=frame_color, fg=text_color, wrap="word", padx=10, pady=10, relief="flat", insertbackground=text_color)
code_text.pack(fill="both", expand=True)

# Output area
output_frame = tk.Frame(main_window, bg=bg_color, bd=0, relief="flat")
output_frame.place(relx=0.03, rely=0.78, relwidth=0.65, relheight=0.18)
output_label = tk.Label(output_frame, text="Output will be shown here.", font=("Consolas", 12), bg=frame_color, fg=text_color, anchor="nw", padx=10, pady=10)
output_label.pack(fill="both", expand=True)

# Variables table
variables_frame = tk.Frame(main_window, bg=bg_color, bd=0)
variables_frame.place(relx=0.7, rely=0.1, relwidth=0.27, relheight=0.65)
tree = ttk.Treeview(variables_frame, columns=("Variable", "Type", "Value"), show="headings")
tree.heading("Variable", text="Variable")
tree.heading("Type", text="Type")
tree.heading("Value", text="Value")
tree.column("Variable", anchor="center", width=80)
tree.column("Type", anchor="center", width=80)
tree.column("Value", anchor="center", width=80)
tree.pack(fill="both", expand=True)

# Tokenized button
button_container = tk.Frame(main_window, bg=bg_color, bd=0)
button_container.place(relx=0.7, rely=0.78, relwidth=0.27, relheight=0.18)
tokenized_button = generate_rounded_button(button_container, "Show Tokenized Output", analyze_code)

# Apply initial theme
apply_theme()

# Start the application
main_window.mainloop()
