from token_container import Tokens
import re

class LexicalAnalyzer:
  """
    Lexical Analyzer Class to tokenize the input code.
    Stores the tokens in a Tokens object.
    In this program, this class tokenizes the input code and stores the tokens in a .tkn file.
  """
  def __init__(self):
    # List of keywords
    self.keywords = ["INT", "STR", "ADD", "SUB", "MULT", "DIV", "MOD", "INTO", "IS", "BEG", "PRINT", "NEWLN", "IOL", "LOI"] # List of keywords
    # List of tokens
    self.tokens = []
    # Output of the Lexical Analyzer
    self.output = {}
    # List of variables
    self.variables = []

  def _isValidKeyword(self, word: str):
    """
      Checks if the word is a valid keyword.
      @param word: The word to be checked.
    """
    return word in self.keywords
  
  def _isValidIdentifier(self, word: str):
    """
      Checks if the word is a valid identifier.
      @param word: The word to be checked.
    """
    return bool(re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9]*$', word))
  
  def _isValidInteger(self, word: str):
    """
      Checks if the word is a valid integer.
      @param word: The word to be checked.
    """
    return bool(re.fullmatch(r'^[0-9]+$', word))

  def _tokenizeWord(self, word: str):
    """
      Tokenizes a single word.
      @param word: The word to be tokenized.
    """
    if self._isValidKeyword(word):
      return "KEYWORD"
    elif self._isValidIdentifier(word):
      return "IDENT"
    elif self._isValidInteger(word):
      return "INT_LIT"
    else:
      return "ERROR"

  def _getDataType(self, previous_token: str):
    """
      Gets the data type of the word.
      @param word: The word to get the data type of.
    """
    return "INT" if previous_token == "INT" else "STR"

  def tokenizeInput(self, input: str):
    """
      Tokenizes the input code and stores the tokens in a Tokens object.
      @param input: The input code to be tokenized.
    """

    # Split the input into lines
    input = input.strip().split("\n")

    for index, line in enumerate(input):
      split_line = line.strip().split(' ')
      tokens = Tokens()

      previous_token = ""

      for word in split_line:
        # Ignore whitespace
        if word == "": continue
        # Remove leading and trailing whitespace
        word = word.strip()
        
        token_type = self._tokenizeWord(word)
        if token_type == "KEYWORD":
          tokens.add_token(word)

        elif token_type == "IDENT":
          data_type = self._getDataType(previous_token)
          if word not in self.variables:
            self.variables.append({
              "name": word,
              "data_type": data_type,
              "value": 0 if data_type == "INT" else ""
            })
          tokens.add_token("IDENT", word)

        elif token_type == "INT_LIT":
          tokens.add_token("INT_LIT", word)

        else:
          tokens.add_token("ERROR", word)
        
        previous_token = word
      self.output[index + 1] = tokens.get_tokens()

  def getVariables(self):
    """
      Gets the variables from the variables list.
    """
    return self.variables
  
  def getOutput(self):
    """
      Gets the output from the output dictionary.
    """
    return self.output

if __name__ == "__main__":
  lexical_analyzer = LexicalAnalyzer()
  lexical_analyzer.tokenizeInput("""
IOL
  INT num IS 0 INT res IS 0
  STR msg1 STR msg2 STR msg3
  BEG msg1 BEG msg2
  BEG msg3
  NEWLN PRINT msg1
  NEWLN
  INTO res IS MULT num num
  PRINT msg2
  PRINT MULT num 2 
  NEWLN
  PRINT msg3
  PRINT res
LOI
""")
  
  print(lexical_analyzer.getVariables())
  print()
  print(lexical_analyzer.getOutput())
  
