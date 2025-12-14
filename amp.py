import json
import pprint
import socket
from enum import Enum, auto

# mpv --idle=yes --no-video --input-ipc-server=/tmp/mpv.sock

class Amp:

 def __init__(self, path="/run/mpv.sock"):
   self.path = path
   self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   self.recv_buffer = b""
   self.track_duration = None
   self.track_position = None
   self.track_album = None
   self.track_artist = None
   self.track_title = None
   self.paused = False
   self.stopped = True
   self.loading = False
   self.eof = True
   self.connect()
   print("Amp initialized.")

 def __del__(self):
   self.disconnect()

 def connect(self):
   self.socket.connect(self.path)
   self.socket.setblocking(False)
   self.mpv_write(["observe_property", 1, "duration"])
   self.mpv_write(["observe_property", 2, "time-pos"])
   self.mpv_write(["observe_property", 3, "album"])
   self.mpv_write(["observe_property", 4, "artist"])
   self.mpv_write(["observe_property", 5, "media-title"])
   self.mpv_write(["observe_property", 6, "pause"])
   print(f"Connected to {self.path}.")

 def disconnect(self):
   self.socket.close()
   print(f"Disconnected from {self.path}.")

 def mpv_write(self, cmds):
   msg = (json.dumps({"command": cmds}) + "\n").encode()
   #print("Write:", msg)
   self.socket.send(msg)

 def mpv_read(self):
   try:
     data = self.socket.recv(4096)
     if data:
       self.recv_buffer += data
       while b"\n" in self.recv_buffer:
         line, self.recv_buffer = self.recv_buffer.split(b"\n", 1)
         msg = json.loads(line)
         #print("mpv recv:", msg)
         if msg.get("event") == "idle":
           self.stopped = True
         elif msg.get("event") == "start-file":
           self.track_position = 0
           self.stopped = False
           self.eof = False
         elif msg.get("event") == "file-loaded":
           self.loading = False
         elif msg.get("event") == "end-file" and msg.get("reason") == "error":
           raise RuntimeError(msg.get("file_error"))
         elif msg.get("event") == "end-file":
           self.eof = True
         elif msg.get("event") == "property-change" and msg.get("name") == "pause":
           self.paused = msg.get("data")
         elif msg.get("event") == "property-change" and msg.get("name") == "duration" and msg.get("data"):
           self.track_duration = msg.get("data")
         elif msg.get("event") == "property-change" and msg.get("name") == "time-pos" and msg.get("data"):
           self.track_position = msg.get("data")
         elif msg.get("event") == "property-change" and msg.get("name") == "album" and msg.get("data"):
           self.track_album = msg.get("data")
         elif msg.get("event") == "property-change" and msg.get("name") == "artist" and msg.get("data"):
           self.track_artist = msg.get("data")
         elif msg.get("event") == "property-change" and msg.get("name") == "media-title" and msg.get("data"):
           self.track_title = msg.get("data")
         #print(f"Paused: {self.paused}, stopped: {self.stopped}, eof: {self.eof}")
   except BlockingIOError:
        pass

 def load_file(self, path):
   self.loading = True
   self.mpv_write(["loadfile", path])

 def play_pause(self):
   if self.paused:
     self.play()
   else:
     self.pause()

 def play(self):
   self.mpv_write(["set_property", "pause", False])

 def pause(self):
   self.mpv_write(["set_property", "pause", True])

 def stop(self):
  self.mpv_write(["stop"])

 def tick(self):
  self.mpv_read()
