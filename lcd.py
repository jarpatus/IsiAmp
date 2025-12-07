import pprint
import math

class Lcd:

 def __init__(self, num_lines=4):
   self.pp = pprint.PrettyPrinter(width=120)
   self.num_lines = num_lines
   self.lines = [""] * num_lines
   print("Lcd initialized.")

 def show_text(self, *lines):
        updated = False
        for i, text in enumerate(lines):
            if i >= self.num_lines:
                break
            if text is not None:
                if self.lines[i] != text:
                  self.lines[i] = text
                  updated = True
        if updated:
          self.pp.pprint(self.lines)
          updated = False


 def show_mounting(self, device):
   self.show_text(
     "Mounting...",
     device,
     "",
     ""
   )


 def show_ejected(self, device):
   self.show_text(
     "Ejected.",
     device,
     "",
     ""
   )

 def show_scanning(self, path, filename):
   self.show_text(
     "Scanning...",
     path,
     filename,
     ""
   )

 def show_playing(self, duration, position, album, artist, title, paused, eof, stopped):
   if stopped:
     self.show_text(
       "Stopped",
       "",
       "",
       ""
     )
   else:
     duration_minutes = math.floor(duration/60)
     duration_seconds = math.floor(duration%60)
     position_minutes = math.floor(position/60)
     position_seconds = math.floor(position%60)
     self.show_text(
       album,
       artist,
       title,
       f"{'⏸' if paused else '▶'} {position_minutes:02d}:{position_seconds:02d} / {duration_minutes:02d}:{duration_seconds:02d}"
     )
