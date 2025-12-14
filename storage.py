import fcntl
import os
import subprocess

CDROM_DRIVE_STATUS = 0x5326
CDS_NO_DISC = 1
CDS_TRAY_OPEN = 2
CDS_DRIVE_NOT_READY = 3
CDS_DISC_OK = 4

class Storage:

 def __init__(self, mediapath, mediadev=None, removable=False):
   self.mediapath = mediapath
   self.mediadev = mediadev
   self.removable = removable
   self.mounted = False if removable else True
   self.available = False if removable else True
   os.makedirs(mediapath, exist_ok=True)
   print("Storage initialized.")

 def mount(self):
    print(f"Mount: {self.removabledev}")
    subprocess.run(["mount", "-o", "ro", "-t", "iso9660,udf", self.removabledev, self.removablepath])
    self.mounted = True

 def umount(self):
    print(f"Un-mount: {self.removabledev}")
    subprocess.run(["umount", "-f", self.removabledev])
    self.mounted = False

 def is_mounted(self):
    return self.mounted

 def eject(self):
    if self.removable_mounted:
      self.umount()
    print(f"Eject: {self.removabledev}")
    subprocess.run(["eject", self.removabledev])
    self.available = False

 def is_removable(self):
    return self.removable

 def is_available(self):
    if not self.mediadev:
      return False
    try:
        with open(self.mediadev, "rb", buffering=0) as fd:
            status = fcntl.ioctl(fd, CDROM_DRIVE_STATUS)
            return status == CDS_DISC_OK
    except:
        return False

 def get_path(self):
    return self.mediapath
