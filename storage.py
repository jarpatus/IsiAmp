import os
import subprocess

class Storage:

 def __init__(self, syspath="/sys/block/sda/sda4", devpath="/dev/sda4", mediapath="/tmp/media", removable=True):
   self.syspath = syspath
   self.devpath = devpath
   self.mediapath = mediapath
   self.removable = removable
   self.available = False if removable else True
   self.mounted = False if removable else True
   os.makedirs(mediapath, exist_ok=True)
   print("Storage initialized using path:", self.devpath)

 def availability_changed(self):
   if not self.removable:
     return False
   if (not self.available and os.path.exists(self.syspath)):
     self.available = True
     print(f"Media {self.devpath} became available.")
     return True
   if (self.available and not os.path.exists(self.syspath)):
     self.available = False
     print(f"Media {self.devpath} became un-available.")
     return False
   return None

 def mount(self):
    if not self.removable:
     return False
    print(f"Mount: {self.devpath}")
    subprocess.run(["mount", self.devpath, self.mediapath])
    self.mounted = True

 def umount(self):
    if not self.removable:
     return False
    print(f"Un-mount: {self.devpath}")
    subprocess.run(["umount", self.devpath])
    self.mounted = False

 def eject(self):
    if not self.removable:
     return False
    if self.mounted:
      self.umount()
    print(f"Eject: {self.devpath}")
    subprocess.run(["eject", self.devpath])
    self.available = False
