import pprint
import math

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

 def show_scanning(self, path, filename):
   self.show_text(
     "Scanning...",
     path,
     filename,
     ""
   )

 def show_playing(self, duration, position, album, artist, title, paused, eof):
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
