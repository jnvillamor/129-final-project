class Compiler:
  def __init__(self):
    self.complete = False

  def compile(self, code):
    """ Compile the source code """

    # Check if the code is valid
    if code == "":
      print("Error: No code to compile")
      return
    
    # Compile the code
    split_code = code.split()
    if (split_code[0] != "IOL" or split_code[-1] != "LOI"):
      raise Exception("Compilation Error! Invalid code format")
      

if __name__ == "__main__":
  compiler = Compiler()
  try:
    compiler.compile("LOI ADD 5 5 LOI")
  except Exception as e:
    print(e)
