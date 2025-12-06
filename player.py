import json
import pprint
import socket

# mpv --idle=yes --no-video --input-ipc-server=/tmp/mpv.sock
class Player:

 def __init__(self, path="/run/mpv.sock"):
   self.pp = pprint.PrettyPrinter(width=120)
   self.path = path
   self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   self.recv_buffer = b""
   self.track_duration = 0
   self.track_position = 0
   self.track_album = None
   self.track_artist = None
   self.track_title = None
   self.track_paused = False
   self.track_eof = False
   print("Player initialized using path:", self.path)

 def connect(self):
   self.socket.connect(self.path)
   self.socket.setblocking(False)
   self.mpv_cmd(["observe_property", 1, "duration"])
   self.mpv_cmd(["observe_property", 2, "time-pos"])
   self.mpv_cmd(["observe_property", 3, "album"])
   self.mpv_cmd(["observe_property", 4, "artist"])
   self.mpv_cmd(["observe_property", 5, "media-title"])
   self.mpv_cmd(["observe_property", 6, "pause"])

 def disconnect(self):
   self.socket.close()

 def mpv_cmd(self, cmds):
   msg = (json.dumps({"command": cmds}) + "\n").encode()
   print("mpv send:", msg)
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
         if msg.get("event") == "property-change" and msg["name"] == "duration":
           self.track_duration = msg["data"] or 0
         elif msg.get("event") == "property-change" and msg["name"] == "time-pos":
           self.track_position = msg["data"] or 0
         elif msg.get("event") == "property-change" and msg["name"] == "album":
           self.track_album = msg["data"]
         elif msg.get("event") == "property-change" and msg["name"] == "artist":
           self.track_artist = msg["data"]
         elif msg.get("event") == "property-change" and msg["name"] == "media-title":
           self.track_title = msg["data"]
         elif msg.get("event") == "property-change" and msg["name"] == "pause":
           self.track_paused = msg["data"]
   except BlockingIOError:
        pass

 def load_file(self, path):
   self.mpv_cmd(["loadfile", path])

 def play_pause(self):
  self.mpv_cmd(["set_property", "pause", not self.track_paused])

 def tick(self):
  self.mpv_read()
