
# CMSC 129 PE03
# by DUYAG, PADERNA, and VILLAMOR

# Libraries
import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
from parser import Parser
import os

# (Overall) Main features:
# 1. Load button: program can take 2 inputs: .prod (productions) file and .ptbl (parse table) file
# 2. Input file tables: Two tables will be used to show the contents of the .prod and .ptbl files
# 2. Status text: (beside load button) displays most recently loaded input file 
# 3. Input bar: user can input a string (sequence of tokens) to be parsed
# 4. Parse button: program will parse the input string using the loaded productions and parse table
# 5. Output: A table will show the solution of the entire parsing process
# 6. Output file: A file of .prsd extension, of CSV format, will be created and saved to store the output table

# Input file notes:
# Both .prod and .ptbl files are of CSV format

# UI starts here.

class ParsingApp:
  """
  Class to create the GUI for the parsing application.
  """
  def __init__(self):
    self.parser = Parser()
    self.input_status = ""
    self.prod_table_file = ""
    self.parse_table_file = ""
    
    # Main window init
    self.main_window = tk.Tk()
    self.main_window.title("PE 03 - Non Recursive Predictive Parsing")
    self.main_window.geometry("900x600")
    
    # Set initial theme to dark mode
    self.bg_color = "#2c2c2c"
    self.text_color = "#ffffff"
    self.button_color = "#0082C8"
    self.frame_color = "#3a3a3a" 
    
    self.main_window.configure(bg=self.bg_color)

    # First Row: Productions and Parse Table
    first_row_frame = tk.Frame(self.main_window, bg=self.bg_color)
    first_row_frame.pack(pady=10, fill="x")

    # Production Table
    self.prod_table_frame = tk.Frame(first_row_frame, bg=self.bg_color)
    self.prod_table_frame.pack(side="left", padx=10)

    self.prod_table_label = tk.Label(self.prod_table_frame, text="Productions: {file_name}", bg=self.bg_color, fg=self.text_color)
    self.prod_table_label.pack(anchor="w")

    self.prod_table = ttk.Treeview(self.prod_table_frame, columns=("ID", "NT", "P"), show="headings", height=10)
    self.prod_table.heading("ID", text="ID")
    self.prod_table.heading("NT", text="NT")
    self.prod_table.heading("P", text="P")
    self.prod_table.pack(fill="both", expand=True)

    # Parse Table
    self.parse_table_frame = tk.Frame(first_row_frame, bg=self.bg_color)
    self.parse_table_frame.pack(side="left", padx=10, fill="both", expand=True)

    self.parse_table_label = tk.Label(self.parse_table_frame, text="Parse Table: {file_name}", bg=self.bg_color, fg=self.text_color)
    self.parse_table_label.pack(anchor="w")

    self.parse_table = ttk.Treeview(self.parse_table_frame, show="headings")
    self.parse_table.pack(fill="both", expand=True)

    # Input Status and Load Button Frame
    status_button_frame = tk.Frame(self.parse_table_frame, bg=self.bg_color)
    status_button_frame.pack(fill="x", pady=5)

    self.input_status = tk.Label(status_button_frame, text="Most recent file: None", bg=self.bg_color, fg=self.text_color)
    self.input_status.pack(side="left")

    self.load_button = tk.Button(status_button_frame, text="Load", command=self.load_file, bg=self.button_color, fg=self.text_color)
    self.load_button.pack(side="right", padx=10)

    # Second Row: Input Bar and Parse Button
    input_frame = tk.Frame(self.main_window, bg=self.bg_color)
    input_frame.pack(pady=10, fill="x")

    self.input_label = tk.Label(input_frame, text="INPUT:", bg=self.bg_color, fg=self.text_color)
    self.input_label.pack(side="left", padx=5)

    self.input_entry = tk.Entry(input_frame, width=50)
    self.input_entry.pack(side="left", padx=5)

    self.parse_button = tk.Button(input_frame, text="Parse", command=self.parse_input, bg=self.button_color, fg=self.text_color)
    self.parse_button.pack(side="left", padx=10)

    # Third Row: Parsing Output Table
    output_frame = tk.Frame(self.main_window, bg=self.bg_color)
    output_frame.pack(pady=10, fill="both", expand=True)

    self.output_status = tk.Label(output_frame, text="Parsing result: None | Output file: None", bg=self.bg_color, fg=self.text_color)
    self.output_status.pack(anchor="w", padx=5, pady=5)

    self.output_table = ttk.Treeview(output_frame, columns=("Stack", "Input Buffer", "Action"), show="headings", height=10)
    self.output_table.heading("Stack", text="Stack")
    self.output_table.heading("Input Buffer", text="Input Buffer")
    self.output_table.heading("Action", text="Action")
    self.output_table.pack(fill="both", expand=True)

  def load_file(self):
      # Placeholder for file loading logic
      pass

  def parse_input(self):
      # Placeholder for parse button functionality
      pass

  def run(self):
      self.main_window.mainloop()

if __name__ == "__main__":
  app = ParsingApp()
  app.run()