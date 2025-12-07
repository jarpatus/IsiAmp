#!/usr/bin/python
import keyboard
import queue
import time
from library import Library
from player import Player
from lcd import Lcd
from storage import Storage

removable = False
#removable = True
mediapath = "/tmp/media" if removable else "./media"
devpath = "/dev/sda4"
syspath = "/sys/block/sda/sda4"


if __name__ == "__main__":
  lcd = Lcd()
  storage = Storage(syspath, devpath, mediapath, removable)
  library = Library(lcd, mediapath)
  player = Player()
  commands = queue.Queue()

  if not removable:
    library.scan()
    player.load_file(library.get_selected_track_path())
    player.play_pause(True)

  i = 0
  keyboard.add_hotkey("7", commands.put, args=("prev_album",))
  keyboard.add_hotkey("6", commands.put, args=("prev_track",))
  keyboard.add_hotkey("5", commands.put, args=("play_pause",))
  keyboard.add_hotkey("4", commands.put, args=("next_track",))
  keyboard.add_hotkey("3", commands.put, args=("next_album",))
  keyboard.add_hotkey("1", commands.put, args=("eject",))
  while True:
   if not commands.empty():
     cmd = commands.get()
     if cmd == "prev_album":
        print("Prev album...")
        if library.prev_album():
          player.load_file(library.get_selected_track_path())
     elif cmd == "prev_track":
        print("Prev track...")
        if library.prev_track():
          player.load_file(library.get_selected_track_path())
     elif cmd == "play_pause":
        print("Play / pause...")
        player.play_pause()
     elif cmd == "next_track":
        print("Next track...")
        if library.next_track():
          player.load_file(library.get_selected_track_path())
     elif cmd == "next_album":
        print("Next album...")
        if library.next_album():
          player.load_file(library.get_selected_track_path())
     elif cmd == "eject":
        print("Eject...")
        lcd.show_ejecting(devpath)
        player.stop()
        if removable:
          library.empty()
          time.sleep(1)
          storage.eject()

   player.tick()
   if player.eof and library.next_track():
     print("EOF");
     player.load_file(library.get_selected_track_path())

   lcd.show_playing(
     player.track_duration,
     player.track_position,
     player.track_album or library.get_selected_album_name(),
     player.track_artist or "Unknown artist",
     player.track_title or library.get_selected_track_name(),
     player.track_paused,
     player.stopped,
     storage.mounted
   )

   if removable and (i % 20) == 0:
     availability = storage.availability_changed()
     if availability == True:
       lcd.show_mounting(devpath)
       storage.mount()
       library.scan()
       player.load_file(library.get_selected_track_path())
       player.play_pause(True)

   i += 1
   time.sleep(0.05)
