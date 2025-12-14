import os


class Album:
  def __init__(self, name, path, tracks):
    self.name = name
    self.path = path
    self.tracks = tracks

  def get_name(self):
    return self.name

  def get_path(self):
    return self.path

  def get_tracks(self):
    return self.tracks

  def get_track(self, index):
    if len(self.tracks) <= index:
      return None
    return self.tracks[index]


class Track:
  def __init__(self, name, path):
    self.name = name
    self.path = path

  def get_name(self):
    return self.name

  def get_path(self):
    return self.path


class Playlist:
  def __init__(self):
    self.albums = []
    self.selected_album_index = 0
    self.selected_track_index = 0
    print("Playlist initialized.")

  def scan(self, path, lcd):
    print(f"Scan: {path}")
    lcd.show_scanning(path)
    self.empty()
    for item in sorted(os.listdir(path)):
        item_path = os.path.abspath(os.path.join(path, item))
        if os.path.isdir(item_path):
            print(f"Album: {item_path}")
            tracks = []
            for f in sorted(os.listdir(item_path)):
                if f.lower().endswith(".mp3"):
                    f_path = os.path.abspath(os.path.join(item_path, f))
                    print(f"\tTrack: {f}")
                    tracks.append(Track(f, f_path))
            if tracks:
               self.albums.append(Album(item, item_path, tracks))

  def empty(self):
    self.albums = []
    self.selected_album_index = 0
    self.selected_track_index = 0

  def prev_album(self, debug=True):
    if self.albums:
      self.selected_album_index -= 1
      self.selected_album_index %= len(self.albums)
      self.selected_track_index = 0
      if debug:
        self.debug_track()
      return True

  def next_album(self, debug=True):
    if self.albums:
      self.selected_album_index += 1
      self.selected_album_index %= len(self.albums)
      self.selected_track_index = 0
      if debug:
        self.debug_track()
      return True

  def prev_track(self):
    tracks = self.get_selected_album_tracks()
    if tracks:
      self.selected_track_index -= 1
      if self.selected_track_index < 0:
        self.prev_album(False)
        self.selected_track_index = len(self.get_selected_album_tracks())-1
      else:
        self.selected_track_index %= len(tracks)
      self.debug_track()
      return True

  def next_track(self):
    tracks = self.get_selected_album_tracks()
    if tracks:
      self.selected_track_index += 1
      if self.selected_track_index >= len(tracks):
        self.next_album(False)
      else:
        self.selected_track_index %= len(tracks)
      self.debug_track()
      return True

  def get_selected_album(self):
    if not self.albums or len(self.albums) <= self.selected_album_index:
      return None
    return self.albums[self.selected_album_index]

  def get_selected_album_tracks(self):
    album = self.get_selected_album()
    if not album:
      return None
    return album.get_tracks()

  def get_selected_track(self):
    album = self.get_selected_album()
    if not album:
      return None
    return album.get_track(self.selected_track_index)

  def has_tracks(self):
    tracks = self.get_selected_album_tracks()
    return tracks and len(tracks) >= 0

  def debug_track(self):
    album = self.get_selected_album()
    track = self.get_selected_track()
    if album:
      print(f"Album {self.selected_album_index+1}/{len(self.albums)} - {album.get_name() if album else None} and track {self.selected_track_index+1}/{len(self.get_selected_album_tracks())} - {track.get_name() if track else None} selected.")
