use_lcd = True
lcd_to_stdout = False

import pprint
import math
if use_lcd:
  from RPLCD.i2c import CharLCD

class Lcd:

 def __init__(self, num_lines=4):
   self.pp = pprint.PrettyPrinter(width=120)
   self.num_lines = num_lines
   self.lines = [""] * num_lines
   if use_lcd:
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
            if text is not None and self.lines[i] != text:
                self.lines[i] = text
                if use_lcd:
                  self.lcd.cursor_pos = (i, 0)
                  self.lcd.write_string(text[:20].ljust(20))
                updated = True
        if updated:
          if lcd_to_stdout:
            self.pp.pprint(self.lines)
          updated = False


 def show_mounting(self, device):
   self.show_text(
     "Mounting media",
     device,
     "",
     "                 ISI"
   )


 def show_ejecting(self, device):
   self.show_text(
     "Ejecting media",
     device,
     "",
     "                 ISI"
   )

 def show_scanning(self, path="", filename=""):
   self.show_text(
     "Scanning media",
     path,
     filename,
     "                 ISI"
   )

 def show_playing(self, amp, storage, playlist):
   if playlist.has_tracks():
     duration_minutes = math.floor((amp.track_duration or 0)/60)
     duration_seconds = math.floor((amp.track_duration or 0)%60)
     position_minutes = math.floor((amp.track_position or 0)/60)
     position_seconds = math.floor((amp.track_position or 0)%60)
     self.show_text(
       f"{playlist.selected_album_index+1}/{len(playlist.albums)} {amp.track_album or playlist.get_selected_album().get_name()}",
       f"{amp.track_artist or 'Unknown artist'}",
       f"{playlist.selected_track_index+1}/{len(playlist.get_selected_album_tracks())} {amp.track_title or playlist.get_selected_track().get_name()}",
       f"{chr(1) if amp.paused else chr(0)} {position_minutes:02d}:{position_seconds:02d} / {duration_minutes:02d}:{duration_seconds:02d}  ISI"
     )
   elif storage.is_removable() and not storage.is_mounted():
     self.show_text("No media", "", "", "                 ISI") 
   else:
     self.show_text("Stopped", "", "", "                 ISI")
