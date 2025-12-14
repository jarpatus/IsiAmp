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

 def set_spin_speed(self, speed=1):
    print(f"Set spin speed to {speed}: {self.mediadev}")
    if not self.mediadev or not self.removable:
      return False
    result = subprocess.run(["eject", "-x", speed, self.mediadev])
    return result.exitcode == 0

 def mount(self):
    print(f"Mount: {self.mediadev}")
    if not self.mediadev or not self.removable:
      return False
    result = subprocess.run(["mount", "-o", "ro", "-t", "iso9660,udf", self.mediadev, self.mediapath])
    if result.exitcode == 0:
      self.mounted = True
      return True
    return False

 def umount(self):
    print(f"Un-mount: {self.mediadev}")
    if not self.mediadev or not self.removable:
      return False
    result = subprocess.run(["umount", "-f", self.mediadev])
    if result.exitcode == 0:
      self.mounted = False
      return True
    return False

 def is_mounted(self):
    return self.mounted

 def eject(self):
    if not self.mediadev or not self.removable:
      return False
    if self.is_mounted():
      if not self.umount():
        return False
    print(f"Eject: {self.mediadev}")
    result = subprocess.run(["eject", self.mediadev])
    if result.exitcode == 0:
      self.available = False
      return True
    return False

 def is_removable(self):
    return self.removable

 def is_available(self):
    if not self.mediadev or not self.removable:
      return False
    try:
        with open(self.mediadev, "rb", buffering=0) as fd:
            status = fcntl.ioctl(fd, CDROM_DRIVE_STATUS)
            return status == CDS_DISC_OK
    except:
        return False

 def get_path(self):
    return self.mediapath
