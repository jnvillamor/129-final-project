class LexicalAnalyzer: 
  
  def __init__(self):
    # Set up the keywords and operators
    keyword_file = open("keywords.txt", "r")
    self.keywords = keyword_file.read().splitlines()
    print(self.keywords)
    
    self.variables = []
    
  def _isValidKeyword(self, input):
    # Return true if input is a keyword, false otherwise
    if input not in self.keywords: return False
    return True
    
  def _isValidVariable(self, input):
    # Return true if variable starts with letter then letter or digit, false otherwise
    if input == "": return False
    if not input[0].isalpha(): return False
    return True
  
  def _isValidInteger(self, input):
    # Return true if input starts with digit, false otherwise
    if input == "": return False
    if not input[0].isdigit(): return False
    return True
  
  def _storeToken(self, token):
    # Store the token in a list
    pass
    
  def _raiseError(self):
    # Raise an error if the input is not valid
    print("Error: Invalid input")

  def tokenizeInput(self, current_input):
    # Iterate through each valid lexeme and return the token
      if self.isValidKeyword(current_input):
        self.storeToken(current_input)
        return current_input
      
      if self.isValidVariable(current_input):
        self.storeToken("IDENT")
        self.variables.append(current_input)
        return "IDENT"
      
      if self.isValidInteger(current_input):
        self.storeToken("INT_LIT")
        return "INT_LIT"
      
      else:
        self.raiseError()
  
if __name__ == "__main__":
  lexical_analyzer = LexicalAnalyzer()