import pprint
import math
from RPLCD.i2c import CharLCD

class Lcd:

 def __init__(self, num_lines=4):
   self.pp = pprint.PrettyPrinter(width=120)
   self.num_lines = num_lines
   self.lines = [""] * num_lines
   self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
   self.lcd.create_char(0, (
    0b01000,
    0b01100,
    0b01110,
    0b01111,
    0b01110,
    0b01100,
    0b01000,
    0b00000,
   ))
   self.lcd.create_char(1, (
    0b11011,
    0b11011,
    0b11011,
    0b11011,
    0b11011,
    0b11011,
    0b11011,
    0b00000,
   ))
   print("Lcd initialized.")

 def show_text(self, *lines):
        updated = False
        for i, text in enumerate(lines):
            if i >= self.num_lines:
                break
            if self.lines[i] != text:
                self.lines[i] = text
                self.lcd.cursor_pos = (i, 0)
                self.lcd.write_string(text[:20].ljust(20))
                updated = True
        if updated:
#          self.pp.pprint(self.lines)
          updated = False


 def show_mounting(self, device):
   self.show_text(
     "Mounting disc",
     device,
     "",
     ""
   )


 def show_ejecting(self, device):
   self.show_text(
     "Ejecting disc",
     device,
     "",
     ""
   )

 def show_scanning(self, path, filename):
   self.show_text(
     "Scanning disc",
     path,
     filename,
     ""
   )

 def show_playing(self, duration, position, album, artist, title, paused, stopped, mounted):
   if not mounted:
     self.show_text("No disc", "", "", "")
   elif stopped:
     self.show_text("Stopped", "", "", "")
   else:
     duration_minutes = math.floor((duration or 0)/60)
     duration_seconds = math.floor((duration or 0)%60)
     position_minutes = math.floor((position or 0)/60)
     position_seconds = math.floor((position or 0)%60)
     self.show_text(
       album,
       artist,
       title,
       f"{chr(1) if paused else chr(0)} {position_minutes:02d}:{position_seconds:02d} / {duration_minutes:02d}:{duration_seconds:02d}  ISI"
     )
