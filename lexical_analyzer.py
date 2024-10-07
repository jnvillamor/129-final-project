class LexicalAnalyzer: 
  
  def __init__(self):
    # Set up the keywords and operators
    keyword_file = open("keywords.txt", "r")
    self.keywords = keyword_file.read().splitlines()
    print(self.keywords)

if __name__ == "__main__":
  lexical_analyzer = LexicalAnalyzer()