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
  lcd = Lcd()
  library = Library(lcd)
  player = Player()
  commands = queue.Queue()

  library.scan()
  player.connect()
  player.load_file(library.get_selected_track_path())
#  update_lcd(player, lcd)

  keyboard.add_hotkey("7", commands.put, args=("prev_album",))
  keyboard.add_hotkey("6", commands.put, args=("prev_track",))
  keyboard.add_hotkey("5", commands.put, args=("play_pause",))
  keyboard.add_hotkey("4", commands.put, args=("next_track",))
  keyboard.add_hotkey("3", commands.put, args=("next_album",))

  while True:
   if not commands.empty():
     cmd = commands.get()
     if cmd == "prev_album":
        print("Prev album...")
        library.prev_album()
        player.load_file(library.get_selected_track_path())
     elif cmd == "prev_track":
        print("Prev track...")
        library.prev_track()
        player.load_file(library.get_selected_track_path())
     elif cmd == "play_pause":
        print("Play / pause...")
        player.play_pause()
     elif cmd == "next_track":
        print("Next tract...")
        library.next_track()
        player.load_file(library.get_selected_track_path())
     elif cmd == "next_album":
        print("Next album...")
        library.next_album()
        player.load_file(library.get_selected_track_path())
   player.tick()
   lcd.show_playing(
     player.track_duration,
     player.track_position,
     player.track_album or library.get_selected_album_name(),
     player.track_artist or "Unknown artist",
     player.track_title or library.get_selected_track_name(),
     player.track_paused,
     player.track_eof,
   )

   time.sleep(0.1)
