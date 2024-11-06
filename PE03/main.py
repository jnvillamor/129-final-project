
# CMSC 129 PE03
# by DUYAG, PADERNA, and VILLAMOR

# Libraries
import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox

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