import json
import pprint
import socket

# mpv --idle=yes --no-video --input-ipc-server=/tmp/mpvsock
class Player:

 def __init__(self, path="/tmp/mpv.sock"):
   self.pp = pprint.PrettyPrinter(width=120)
   self.path = path
   self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   self.playing = False
   print("Player initialized using path:", self.path)

 def connect(self):
   self.socket.connect(self.path)
   self.mpv_cmd(["set_property", "pause", True])

 def disconnect(self):
   self.socket.close()

 def mpv_cmd(self, cmds): 
   msg = {"command": cmds}
   self.socket.send((json.dumps(msg) + "\n").encode())

 def load_file(self, path):
   self.mpv_cmd(["loadfile", path])

 def play(self):
  self.playing = True
  self.mpv_cmd(["set_property", "pause", not self.playing])

 def pause(self):
  self.playing = False
  self.mpv_cmd(["set_property", "pause", not self.playing])

 def play_pause(self):
  self.playing = not self.playing
  self.mpv_cmd(["set_property", "pause", not self.playing])

 def is_playing(self):  
  return self.playing
