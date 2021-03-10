from os import listdir
import os
import platform
import shutil
import ctypes

# NOTE: - Adopted From StackOverFLow Post: https://stackoverflow.com/a/17030773/6427171


drives = []
system = platform.system()

# drive types
DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
DRIVE_NO_ROOT_DIR = 1  # The root path is invalid; for example, there is no volume mounted at the specified path.
DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
DRIVE_FIXED       = 3  # The drive has fixed media; for example, a hard disk drive or flash drive.
DRIVE_REMOTE      = 4  # The drive is a remote (network) drive.
DRIVE_CDROM       = 5  # The drive is a CD-ROM drive.
DRIVE_RAMDISK     = 6  # The drive is a RAM disk.

# map drive types to strings
DRIVE_TYPE_MAP = { DRIVE_UNKNOWN     : 'DRIVE_UNKNOWN',
                   DRIVE_NO_ROOT_DIR : 'DRIVE_NO_ROOT_DIR',
                   DRIVE_REMOVABLE   : 'DRIVE_REMOVABLE',
                   DRIVE_FIXED       : 'DRIVE_FIXED',
                   DRIVE_REMOTE      : 'DRIVE_REMOTE',
                   DRIVE_CDROM       : 'DRIVE_CDROM',
                   DRIVE_RAMDISK     : 'DRIVE_RAMDISK'}


# return list of tuples mapping drive letters to drive types
def get_drive_info():
    result = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        bit = 2 ** i
        if bit & bitmask:
            drive_letter = '%s:' % chr(65 + i)
            drive_type = ctypes.windll.kernel32.GetDriveTypeW('%s\\' % drive_letter)
            result.append((drive_letter, drive_type))
    return result

# return list of system drives
def get_system_drives():
    drive_info = get_drive_info()
    # for drive_letter, drive_type in drive_info:
    #     print('%s = %s' % (drive_letter, DRIVE_TYPE_MAP[drive_type]))
    return [drive_letter for drive_letter, drive_type in drive_info if drive_type == DRIVE_FIXED]

# returns a tuple of a disk's total files and folders count.
def get_folder_and_files_total(directory):
    files = folders = 0

    for _, dirnames, filenames in os.walk(directory):
    # ^ this idiom means "we won't be using this value"
        files += len(filenames)
        folders += len(dirnames)

    print('{:,} files, {:,} folders'.format(files, folders))

    return files, folders

# Returns a tuple of a disk's total, used, and free space.
def get_disk_info(drive):
    total, used, free = shutil.disk_usage(drive)
    total = total // (1024.0 ** 3)
    used = used // (1024.0 ** 3)
    free = free // (1024.0 ** 3)
    return total, used, free

def dump_drives():
    if 'Darwin' in system:
        print('MacOS')
        for drive in listdir('/Volumes'):
            print(drive, get_folder_and_files_total('/Volumes/' + drive), get_disk_info('/Volumes/' + drive))
    elif 'Linux' in system:
        print("Linux")
    elif 'Windows' in system:
        print("Windows")
        drives.extend(get_system_drives())
        print(drives)
        for drive in drives:
            print(drive, get_folder_and_files_total(drive), get_disk_info(drive))