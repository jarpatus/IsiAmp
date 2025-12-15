#!/usr/bin/python
import keyboard
import queue
import time
import sys
import fcntl
import os
import termios
import select
from getchar import getkeys
from lcd import Lcd
from storage import Storage
from playlist import Playlist
from amp import Amp

sources = [
  {"name": "Internal1", "path": "./media", "device": None, "removable": False},
#  {"name": "Internal2", "path": "./media2", "device": None, "removable": True},
  {"name": "Removable", "path": "/media/cdrom", "device": "/dev/cdrom", "removable": True},
]

use_stdin = False

def scan_and_play(storage, lcd, amp):
  playlist.scan(storage.get_path(), lcd)
  track = playlist.get_selected_track()
  if track:
    amp.load_file(track.get_path())
    amp.play()

def full_stop(amp, library):
  amp.stop()
  library.empty()

if __name__ == "__main__":
  source_index = 0

  # Instantiate our classes
  lcd = Lcd()
  storage = Storage(sources[source_index]["path"], sources[source_index]["device"], sources[source_index]["removable"])
  playlist = Playlist()
  amp = Amp()
  commands = queue.Queue()

  # Add hotkey handlers for USB keyboards
  keyboard.add_hotkey("1", commands.put, args=("prev_album",))
  keyboard.add_hotkey("2", commands.put, args=("prev_track",))
  keyboard.add_hotkey("3", commands.put, args=("play_pause",))
  keyboard.add_hotkey("4", commands.put, args=("next_track",))
  keyboard.add_hotkey("5", commands.put, args=("next_album",))
  keyboard.add_hotkey("6", commands.put, args=("source",))
  keyboard.add_hotkey("7", commands.put, args=("eject",))
  keyboard.add_hotkey("8", commands.put, args=("stop_scan",))

  # Create playlist and start playing from first file
  scan_and_play(storage, lcd, amp)

  # Main loop
  i = 0
  while True:

    # Read stdin so we can debug over ssh
    if use_stdin:
     keys = getkeys()
     for key in keys:
      if key == "1":
       commands.put("prev_album")
      elif key == "2":
       commands.put("prev_track")
      elif key == "3":
       commands.put("play_pause")
      elif key == "4":
       commands.put("next_track")
      elif key == "5":
       commands.put("next_album")
      elif key == "6":
       commands.put("source")
      elif key == "7":
       commands.put("eject")
      elif key == "8":
       commands.put("stop_scan")

    # Process commands queue (async safe)
    if not commands.empty():
     while not commands.empty():
       cmd = commands.get()
     if cmd == "prev_album":
        print("Prev album...")
        if playlist.prev_album():
          amp.load_file(playlist.get_selected_track().get_path())
     elif cmd == "prev_track":
        print("Prev track...")
        if playlist.prev_track():
          amp.load_file(playlist.get_selected_track().get_path())
     elif cmd == "play_pause":
        print("Play / pause...")
        amp.play_pause()
     elif cmd == "next_track":
        print("Next track...")
        if playlist.next_track():
          amp.load_file(playlist.get_selected_track().get_path())
     elif cmd == "next_album":
        print("Next album...")
        if playlist.next_album():
          amp.load_file(playlist.get_selected_track().get_path())
     elif cmd == "stop_scan":
        print("Stop / scan...")
        if amp.stopped:
          scan_and_play(storage, lcd, amp)
        else:
          full_stop(amp, playlist)
     elif cmd == "source":
        print("Source...")
        full_stop(amp, playlist)
        source_index += 1
        source_index %= len(sources)
        storage = Storage(sources[source_index]["path"], sources[source_index]["device"], sources[source_index]["removable"])
        if not storage.is_removable():
          scan_and_play(storage, lcd, amp)
     elif cmd == "eject":
        print("Eject...")
        lcd.show_ejecting(storage.get_path())
        full_stop(amp, playlist)
        if storage.is_removable():
          storage.eject()

    # Tick amp (it is synchronous so we need to read messages from IPC like this)
    amp.tick()

    # Select next track on EOF
    if not amp.loading and amp.eof and amp.stopped and not amp.paused and playlist.next_track():
     print("EOF")
     amp.load_file(playlist.get_selected_track().get_path())

    # Mount removable storage if needed
    if (i % 20) == 0 and storage.is_removable() and not storage.is_mounted() and storage.is_available():
       lcd.show_mounting(storage.get_device())
       if storage.mount():
         storage.set_spin_speed()
         scan_and_play(storage, lcd, amp)

    # Update LCD
    lcd.show_playing(amp, storage, playlist)

#   print(".")
    i += 1
    time.sleep(0.05)
