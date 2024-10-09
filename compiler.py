from lexical_analyzer import LexicalAnalyzer

class Compiler:
  def __init__(self):
    self.lexical_analyzer = LexicalAnalyzer()
    self.tokenize_code = ""
  
  def compile(self, code: str):
    """ Compile the source code """

    # Check if the code is valid
    if code == "":
      print("Error: No code to compile")
      return
    
    # Compile the code
    code = code.strip() 
    split_code = code.split('\n')

    if (not split_code[0].strip().split()[0] == 'IOL'):
      raise Exception("Error: Invalid code")
    
    if (not split_code[-1].strip().split()[-1] == 'LOI'):
      raise Exception("Error: Invalid code")
    
    # Remove the IOL and LOI
    split_code[0] = split_code[0].replace('IOL', '')
    split_code[-1] = split_code[-1].replace('LOI', '')

    final_input = "\n".join(split_code)
    self.lexical_analyzer.tokenizeInput(final_input)

if __name__ == "__main__":
  input = """
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
  """
  
  compiler = Compiler()
  compiler.compile(input)
  
    

