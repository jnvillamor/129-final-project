class LexicalAnalyzer: 
  
  def __init__(self):
    # Set up the keywords and operators
    keyword_file = open("keywords.txt", "r")
    self.keywords = keyword_file.read().splitlines()
    
    self.variables = [] # Variables stored for IDENT table
    self.current_input = "" # Current code input for Lexical Analyzer
    self.output = "" # Output of the Lexical Analyzer
  
  def _isValidKeyword(self, input):
    # Return true if input is a keyword, false otherwise
    if input not in self.keywords: return False
    return True
    
  def _isValidVariable(self, input):
    # Return true if variable starts with letter then letter or digit, false otherwise
    if input == "": return False
    if not input[0].isalpha(): return False
    for char in input: # Must only contain letters and digits
      if not char.isalnum(): return False
    return True
  
  def _isValidInteger(self, input):
    # Return true if input starts with digit, false otherwise
    if input == "": return False
    if not input[0].isdigit(): return False
    return True
  
  def _storeToken(self, token):
    # Store the token in a list
    pass
  
  def writeOutput(self):
    # Write the output of tokenization to a .tkn extension file
    output_file = open("output.tkn", "w")
    output_file.write(self.output)
    output_file.close()
  
  def _raiseError(self):
    # Raise an error if the input is not valid
    print("Error: Invalid input")

  def tokenizeInput(self, current_input):
      current_input = current_input.split("\n")
      
      # Iterate through each word on each line of the input
      for line in current_input:
        if line == "": continue
        tokenized_line = ""
        for word in line.split():
          tokenized_line += self.tokenizeWord(word) + " "
        self.output += tokenized_line + "\n"    
      
      # Write output after tokenization
      self.writeOutput()
                 
  def tokenizeWord(self, current_input):
    # Iterate through each valid lexeme and return the token
      if self._isValidKeyword(current_input):
        self._storeToken(current_input)
        return current_input
      
      if self._isValidVariable(current_input):
        self._storeToken("IDENT")
        self.variables.append(current_input)
        return "IDENT"
      
      if self._isValidInteger(current_input):
        self._storeToken("INT_LIT")
        return "INT_LIT"
      
      else:
        self._raiseError()
  
if __name__ == "__main__":
  lexical_analyzer = LexicalAnalyzer()