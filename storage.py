import fcntl
import os
import subprocess

CDROM_DRIVE_STATUS = 0x5326
CDS_NO_DISC = 1
CDS_TRAY_OPEN = 2
CDS_DRIVE_NOT_READY = 3
CDS_DISC_OK = 4

class Storage:

 def __init__(self, devpath="/dev/cdrom", mediapath="/media/cdrom", removable=True):
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
   if (not self.available and self.has_disc()):
     self.available = True
     print(f"Media {self.devpath} became available.")
     return True
   #if (self.available and not has_disc()):
   #  self.available = False
   #  print(f"Media {self.devpath} became un-available.")
   #  return False
   return None

 def mount(self):
    if not self.removable:
     return False
    print(f"Mount: {self.devpath}")
    subprocess.run(["mount", "-o", "ro", "-t", "iso9660,udf", self.devpath, self.mediapath])
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

 def has_disc(self):
    try:
        with open(self.devpath, "rb", buffering=0) as fd:
            status = fcntl.ioctl(fd, CDROM_DRIVE_STATUS)
            return status == CDS_DISC_OK
    except:
        return False
