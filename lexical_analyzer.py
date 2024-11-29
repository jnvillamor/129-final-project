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
    # Errors list
    self.errors = []

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
    if self._isValidKeyword(word): # If the word is a keyword, return KEYWORD
      return "KEYWORD"
    elif self._isValidIdentifier(word): # If the word is an identifier, return IDENT
      return "IDENT"
    elif self._isValidInteger(word): # If the word is an integer literal, return INT_LIT
      return "INT_LIT"
    else: # If the word is invalid, return ERROR
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

    # Tokenize each line of the input
    for index, line in enumerate(input):
      split_line = line.strip().split(' ')
      tokens = Tokens()

      previous_token = ""

      # Tokenize each word in the line
      for word in split_line:
        # Ignore whitespace
        if word == "": continue
        # Remove leading and trailing whitespace
        word = word.strip()
        
        token_type = self._tokenizeWord(word)
        if token_type == "KEYWORD": # If the word is a keyword, add it to the tokens
          tokens.add_token(word)

        elif token_type == "IDENT": # If the word is an identifier, add it to the variables list
          data_type = self._getDataType(previous_token)
          flag = False

          for variable in self.variables: # Check if the variable is already in the variables list
            if variable["name"] == word: 
              flag = True
              break

          if not flag: # If the variable is not already in the variables list, add it
            self.variables.append({"name": word, "data_type": data_type, "value": 0 if data_type == "INT" else ""})

          tokens.add_token("IDENT", word)

        elif token_type == "INT_LIT": # If the word is an integer literal, add it to the tokens
          tokens.add_token("INT_LIT", word)

        else: # If the word is invalid, add it to the errors list
          tokens.add_token("ERROR", word)
          self.errors.append(f"Error on line {index + 1} | Invalid word: {word}")
        
        previous_token = word
      
      # Add the tokens to the output dictionary
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