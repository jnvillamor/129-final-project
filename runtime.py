import tkinter as tk

## Remaining Tasks
# Implement BEG 
# - [ ] user input
# - [ ] update symbol table

# Dynamic Semantic Analysis
#- [ ] type checking of 2 operands (from BEG)
class Runtime:
    def __init__(self, code_text_widget, console_text_widget, symbol_table):
        self.code_text_widget = code_text_widget
        self.console_text_widget = console_text_widget
        self.symbol_table = symbol_table
        self.input_var_name = None

    def process_input_code(self, tokens: dict):
        
        is_beg_command = False
        is_print_command = False
        awaiting_input = False

        for line_number, token in tokens.items():
            len_token = len(token)
            current_token_index = 0
            
            while current_token_index < len_token:
                command = token[current_token_index]
                word = command["name"]
                value = command["value"]
                
                if word == "BEG":
                    is_beg_command = True
                
                elif is_beg_command:
                    # Get the next token
                    current_token_index += 1
                    next_token = token[current_token_index]
                    
                    self.input_var_name = next_token["value"]
                    
                    # Enable console for input
                    self.console_text_widget.config(state=tk.NORMAL)
                    self.console_text_widget.bind("<Return>", self.capture_input)
                    
                    # Disable further editing
                    self.code_text_widget.config(state=tk.DISABLED)
                    
                    is_beg_command = False
                    
                current_token_index += 1
                    
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, "\n\n Program terminated successfully...")
        self.console_text_widget.config(state=tk.DISABLED)
        
    def capture_input(self, event):
        """
            Waits for the user to input a value and stores it in the symbol table.
        """
        # Get the last line of text from the console (user input)
        input_text = self.console_text_widget.get("end-2c linestart", "end-1c")
        
        # Only process if there's actual input
        if input_text.strip():
            print(f"Input for {self.input_var_name}: {input_text}")
            # Update the symbol table with user input
            self.symbol_table.get_symbol(self.input_var_name)["value"] = input_text
            # Disable further editing and unbind the Return key event
            self.console_text_widget.config(state=tk.DISABLED)
            self.console_text_widget.unbind("<Return>")
            # Resume processing after input is captured
            self.process_input_code(self.tokens)  # Re-process the tokens
            return input_text
