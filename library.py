import os
import pprint 

class Library:

  def __init__(self, lcd, path="./media"):
    self.pp = pprint.PrettyPrinter(width=120)
    self.lcd = lcd
    self.path = path
    self.albums = []
    self.selected_album_index = 0
    self.selected_track_index = 0
    print("Library initialized using path:", self.path)

  def scan(self):
    self.albums = []
    for item in sorted(os.listdir(self.path)):
        item_path = os.path.abspath(os.path.join(self.path, item))
        if os.path.isdir(item_path):
            self.lcd.show_scanning(item, "")
            tracks = []
            for f in sorted(os.listdir(item_path)):
                if f.lower().endswith(".mp3"):
                    self.lcd.show_scanning(item, f)
                    f_path = os.path.abspath(os.path.join(item_path, f))
                    tracks.append({"name": f, "path": f_path})
            if tracks:
               self.albums.append({"name": item, "path": item_path, "tracks": tracks})
    self.pp.pprint(self.albums)

  def prev_album(self):
    self.selected_album_index -= 1
    self.selected_album_index %= len(self.albums)
    self.selected_track_index = 0
    self.track_selected()

  def next_album(self):
    self.selected_album_index += 1
    self.selected_album_index %= len(self.albums)
    self.selected_track_index = 0
    self.track_selected()

  def prev_track(self):
    self.selected_track_index -= 1
    self.selected_track_index %= len(self.get_selected_album_tracks())
    self.track_selected()

  def next_track(self):
    self.selected_track_index += 1
    self.selected_track_index %= len(self.get_selected_album_tracks())
    self.track_selected()

  def track_selected(self):
    print(f"Album {self.get_selected_album_name()} and track {self.get_selected_track_name()} selected.")
  
  def get_albums(self):
    return self.albums

  def get_selected_album(self):
    return self.albums[self.selected_album_index]

  def get_selected_album_index(self):
    return self.selected_album_index

  def get_selected_album_name(self):
    return self.get_selected_album()["name"]

  def get_selected_album_tracks(self):
    return self.get_selected_album()["tracks"]

  def get_selected_track(self):
    return self.get_selected_album_tracks()[self.selected_track_index]

  def get_selected_track_index(self):
    return self.selected_track_index

  def get_selected_track_path(self):
    return self.get_selected_track()["path"] 

  def get_selected_track_name(self):
    return self.get_selected_track()["name"]
