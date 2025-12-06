import pprint

class Lcd:

 def __init__(self, num_lines=4):
   self.pp = pprint.PrettyPrinter(width=120)
   self.num_lines = num_lines
   self.lines = [""] * num_lines
   print("Lcd initialized.")

 def show_text(self, *lines): 
        for i, text in enumerate(lines):
            if i >= self.num_lines:
                break
            if text is not None:
                self.lines[i] = text
        self.pp.pprint(self.lines)
