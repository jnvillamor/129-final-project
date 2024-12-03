import tkinter as tk

class Runtime:
    def __init__(self, code_text_widget, console_text_widget, symbol_table):
        self.code_text_widget = code_text_widget
        self.console_text_widget = console_text_widget
        self.symbol_table = symbol_table
        self.output_text = ""
        self.input_var_name = None

    def process_input_code(self):
        code = self.code_text_widget.get(1.0, tk.END).strip().split("\n")
        
        for line in code:
            tokens = line.strip().split()
            if not tokens:
                continue

            command = tokens[0]
            if command == "BEG":
                self.input_var_name = tokens[1]
                self.console_text_widget.insert(tk.END, f"Input for {self.input_var_name}: ")
                self.console_text_widget.bind("<Return>", self.capture_input)
                return  # Wait for user input

            elif command == "NEWLN":
                self.output_text += "\n\n"

            elif command == "PRINT":
                var_name = tokens[1]
                var_value = self.symbol_table.get_symbol(var_name)["value"]
                self.output_text += f"{var_value} "

        self.output_text += "\n\n Program terminated successfully..."
        self.console_text_widget.delete(1.0, tk.END)
        self.console_text_widget.insert(tk.END, self.output_text)

    def capture_input(self, event):
        user_input = self.console_text_widget.get("end-2c linestart", "end-1c").strip()
        self.symbol_table.add_symbol(self.input_var_name, "STR", user_input)
        self.output_text += f"Input for {self.input_var_name}: {user_input}\n"
        self.console_text_widget.unbind("<Return>")
        self.process_input_code()  # Continue processing the rest of the code