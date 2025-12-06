#!/usr/bin/python
import keyboard
import queue
import time
from library import Library
from player import Player
from lcd import Lcd

def update_lcd(player, lcd): 
  lcd.show_text(
	f"{library.get_selected_album_index()+1}/{len(library.get_albums())} {library.get_selected_album_name()}",
	f"{library.get_selected_track_index()+1}/{len(library.get_selected_album_tracks())} {library.get_selected_track_name()}",
        "Playing..." if player.is_playing() else "Paused" 
  )

if __name__ == "__main__":
  library = Library()
  player = Player()
  lcd = Lcd()
  commands = queue.Queue()

  lcd.show_text("Scanning...", "", "", "")
  library.scan()
  player.connect()
  player.load_file(library.get_selected_track_path())
  update_lcd(player, lcd)

  keyboard.add_hotkey("q", commands.put, args=("prev_album",))
  keyboard.add_hotkey("w", commands.put, args=("prev_track",))
  keyboard.add_hotkey("e", commands.put, args=("play_pause",))
  keyboard.add_hotkey("r", commands.put, args=("next_track",))
  keyboard.add_hotkey("t", commands.put, args=("next_album",))

  while True:
   if not commands.empty():
    cmd = commands.get()
    match cmd:

     case "prev_album":
        library.prev_album()
        player.load_file(library.get_selected_track_path())

     case "prev_track":
        library.prev_track()
        player.load_file(library.get_selected_track_path())

     case "play_pause":
        player.play_pause()

     case "next_track":
        library.next_track()
        player.load_file(library.get_selected_track_path())

     case "next_album":
        library.next_album()
        player.load_file(library.get_selected_track_path())

   time.sleep(0.1)
