# CMSC 129 PE03
# by DUYAG, PADERNA, and VILLAMOR

# Libraries
import tkinter as tk
from tkinter import ttk, filedialog, messagebox 
from parser import Parser

'''
Class to create the GUI for the parsing application.
'''
class ParsingApp:
  def __init__(self):
    self.parser = Parser()
    self.input_status = ""
    self.prod_table_file_name = ""
    self.prod_table_file = ""
    self.ptbl_file = ""
    
    ### Main window init
    self.main_window = tk.Tk()
    self.main_window.title("PE 03 - Non Recursive Predictive Parsing")
    self.main_window.geometry("900x600")
    self.main_window.state("zoomed")  # Default window size to fullscreen
    # Dark mode GUI theme for eye comfort
    self.bg_color = "#2c2c2c"
    self.text_color = "#ffffff"
    self.button_color = "#0082C8"
    self.frame_color = "#3a3a3a" 
    self.main_window.configure(bg=self.bg_color)

    ### First row frame: production & parse table
    first_row_frame = tk.Frame(self.main_window, bg=self.bg_color)
    first_row_frame.pack(pady=10, fill="x")

    # Production Table
    self.prod_table_frame = tk.Frame(first_row_frame, bg=self.bg_color)
    self.prod_table_frame.pack(side="left", padx=10)
    # Dynamic label based on loaded file
    self.prod_table_label = tk.Label(self.prod_table_frame, text="Productions: ", bg=self.bg_color, fg=self.text_color)
    self.prod_table_label.pack(anchor="w")
    # Create Treeview widget for prod_table
    self.prod_table = ttk.Treeview(self.prod_table_frame, columns=("ID", "NT", "P"), show="headings", height=10)
    self.prod_table.heading("ID", text="ID")  # ID is the index of the production
    self.prod_table.heading("NT", text="NT")  # NT is the non-terminal symbol
    self.prod_table.heading("P", text="P")    # P is the production rule
    self.prod_table.pack(fill="both", expand=True)

    # Parse Table
    self.parse_table_frame = tk.Frame(first_row_frame, bg=self.bg_color)
    self.parse_table_frame.pack(side="left", padx=10, fill="both", expand=True)
    # Dynamic label based on loaded file
    self.parse_table_label = tk.Label(self.parse_table_frame, text="Parse Table: ", bg=self.bg_color, fg=self.text_color)
    self.parse_table_label.pack(anchor="w")
    # Create Treeview widget for parse_table
    self.parse_table = ttk.Treeview(self.parse_table_frame, show="headings")
    self.parse_table.pack(fill="both", expand=True)

    # Frame for input status and load button
    status_button_frame = tk.Frame(self.parse_table_frame, bg=self.bg_color)
    status_button_frame.pack(fill="x", pady=5)
    # Input status label
    self.input_status = tk.Label(status_button_frame, text="Most recent file: None", bg=self.bg_color, fg=self.text_color)
    self.input_status.pack(side="left")
    # Load button
    self.load_button = tk.Button(status_button_frame, text="Load", command=self.loadFile, bg=self.button_color, fg=self.text_color)
    self.load_button.pack(side="right", padx=10)
    self.main_window.bind("<Control-o>", lambda event: self.loadFile())  # Shortcut key for load button

    ### Second row frame: input text bar and parse button
    input_frame = tk.Frame(self.main_window, bg=self.bg_color)
    input_frame.pack(pady=10, fill="x")
    self.input_label = tk.Label(input_frame, text="INPUT:", bg=self.bg_color, fg=self.text_color)
    self.input_label.pack(side="left", padx=5)
    # Input entry
    self.input_entry = tk.Entry(input_frame, width=50)
    self.input_entry.pack(side="left", padx=5)
    # Parse button
    self.parse_button = tk.Button(input_frame, text="Parse", command=self.parseInput, bg=self.button_color, fg=self.text_color)
    self.parse_button.pack(side="left", padx=10)

    ### Last row frame: output table
    output_frame = tk.Frame(self.main_window, bg=self.bg_color)
    output_frame.pack(pady=10, fill="both", expand=True)
    # Output status label
    self.output_status = tk.Label(output_frame, text="Parsing result: None | Output file: None", bg=self.bg_color, fg=self.text_color)
    self.output_status.pack(anchor="w", padx=5, pady=5)
    # Create Treeview widget for output_table
    self.output_table = ttk.Treeview(output_frame, columns=("Stack", "Input Buffer", "Action"), show="headings", height=10)
    self.output_table.heading("Stack", text="Stack")
    self.output_table.heading("Input Buffer", text="Input Buffer")
    self.output_table.heading("Action", text="Action")
    self.output_table.pack(fill="both", expand=True)

  '''
  loadFile(self: ParsingApp) -> None
  Function to load a file from the file system and display its contents to the GUI based on the file type.
  The file can only be of type .prod (productions) or .ptbl (parse table).
  '''
  def loadFile(self):
    # Open file dialog with restricted file types
    input_file = filedialog.askopenfilename(filetypes=[("InputFiles", "*.prod *.ptbl")])

    # Deconstruct the input file to get the file type, file name, and content
    filetype, file_name, content = self.parser.getInput(input_file)
    
    # Prod table - display the content to the appropriate table
    if filetype == "prod":
      self.prod_table_label.config(text=f"Productions: {file_name}") # Update label based on file name
      
      for i in content: # Load content tuple to prod table
        self.prod_table.insert("", "end", values=i)
      
      self.prod_table_file_name = file_name.split('.')[0] # save the file name for output file naming
        
    # Parse table - display the content to the appropriate table
    elif filetype == "ptbl":
      self.parse_table_label.config(text=f"Parse Table: {file_name}") # Update label based on file name

      # Define table dimensions based on parse table content
      num_col = len(content[0])

      # Config parse_table columns with first row of content
      self.parse_table["columns"] = content[0]
      
      for i in range(num_col):  # Add column headings
        self.parse_table.heading(content[0][i], text=content[0][i])
      
      for i in content[1:]: # Load content tuple to parse table, skipping the first row (from defined terminal headings)
        self.parse_table.insert("", "end", values=i)
            
    self.input_status.config(text=f"LOADED: {file_name}") # Update input status label 
  
  '''
  parseInput(self: ParsingApp) -> None
  Function to parse the input string based on the loaded productions and parse table.
  The output will be displayed to the output table and saved to a .prsd file.
  '''
  def parseInput(self):
    input_string = self.input_entry.get() # Get input string from input entry
    
    # If no production or parse table is loaded, prompt user to load a file
    if self.prod_table_label.cget("text") == "Productions: " or self.parse_table_label.cget("text") == "Parse Table: ":
      self.output_status.config(text="Parsing result: Failed | Load a production and parse table file first.")
      # Tkinter error message box
      tk.messagebox.showerror("Error", "Load a production and parse table file first.")
      return
    
    output = self.parser.parse(input_string) # Parse the input string
    
    self.printOutput(output) # Display the output to the output table and save to a .prsd file
    
  '''
  printOutput(self: ParsingApp, output: list) -> None
  Function to display the output to the output table and save the output to a .prsd file.
  The function takes in the parsed output as a list of lists.
  '''
  def printOutput(self, output):
    for i in output: # Load content tuple to output table
      self.output_table.insert("", "end", values=i)
    
    # Configure output filename
    output_filepath = filedialog.asksaveasfilename(defaultextension=f".prsd", filetypes=[("OutputFiles", "*.prsd")])
    output_filename = f"{output_filepath.split('/')[-1].split('.')[0]}_{self.prod_table_file_name}" # outname_prodname file format
    
    self.parser.exportOutput(output_filename) # Save output to .prsd file
    
    # Update output status label
    self.output_status.config(text=f"Parsing result: Success | Output file: {output_filename}.prsd")
    
  # Run the main window
  def run(self):
      self.main_window.mainloop()

# Main function
if __name__ == "__main__":
  app = ParsingApp()
  app.run()