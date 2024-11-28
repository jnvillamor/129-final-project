class Tokens:
  def __init__(self):
    self.tokens = []
  
  def add_token(self, name, value = None):
    self.tokens.append({
      "name": name,
      "value": value
    })

  def get_tokens(self):
    return self.tokens
  