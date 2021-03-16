# PURP: - TO HANDLE DRIVE INFO LOGIC FOR -d and --drv arguments
from os import listdir, walk, path
from constants import *   
from helper import format_size
import logging
import platform
import shutil
import ctypes

logging.debug('Logging in drive_dump.py')


system = platform.system()

# return list of tuples mapping drive letters to drive types
# NOTE: - Adopted From StackOverFLow Post: https://stackoverflow.com/a/17030773/6427171
def get_drive_info():
    result = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        bit = 2 ** i
        if bit & bitmask:
            drive_letter = '%s:' % chr(65 + i)
            drive_type = ctypes.windll.kernel32.GetDriveTypeW('%s\\' % drive_letter)
            logging.debug("Drive %s Detected." % drive_letter)
            result.append((drive_letter, drive_type))
    return result

# return list of system drives
def get_system_drives():
    try:
        drive_info = get_drive_info()
    except Exception:
        logging.critical("Cannot get system's drives")
        return None
    return [drive_letter for drive_letter, drive_type in drive_info if drive_type == DRIVE_FIXED]

# returns a tuple of a disk's total files and folders count.
def get_folder_and_files_total(directory):
    
    files = folders = 0
    try:
        for _, dirnames, filenames in walk(directory):
            files += len(filenames)
            folders += len(dirnames)
    except Exception:
        logging.critical("Cannot get count of drive's files and folders")
        return None, None
    if files < 0:
        logging.error("File count less than 0")
        return None, None
    if folders < 0:
         logging.error("Folder count less than 0")
         return None, None

    # logging.debug('{:,} files, {:,} folders'.format(files, folders))
    return files, folders

# Returns a tuple of a disk's total, used, and free space.
def get_disk_info(drive):
    try:
        total, used, free = shutil.disk_usage(drive)
    except Exception:
        logging.critical("Cannot get drive's storage info")
        return None, None, None
    try:
        total = format_size(total)
        used = format_size(used)
        free = format_size(free)
    except Exception:
        logging.error(COMP_ERROR)
        return None, None, None
    return total, used, free

def macos_dump():
    logging.debug(MACOS_DETECTED)
    drive_info = []
    try: 
        for drive in listdir('/Volumes'):
            logging.debug("Beginning Info Dumping of: %s" % drive)
            drive_info.append((drive, get_folder_and_files_total('/Volumes/' + drive), get_disk_info('/Volumes/' + drive)))
        return drive_info
    except Exception:
        logging.critical(MACOS_CRITICAL)
        return None

def linux_dump():
    logging.debug(LINUX_DETECTED)
    return None

def windows_dump():
    logging.debug(WINDOWS_DETECTED)
    drive_info = []
    try:
        drives = get_system_drives()
        if drives is None:
            logging.critical(WINDOWS_CRITICAL)
            return None
        else:
            for drive in drives:
                logging.debug("Beginning Info Dumping of: %s" % drive)
                drive_info.append((drive, get_folder_and_files_total(drive), get_disk_info(drive)))
            return drive_info
    except Exception:
        logging.critical(WINDOWS_CRITICAL)
        return None

# Master Function that returns the info of all of a system's drives
# For MacOS, the function reads all drives in /Volumes.
# For Windows, the function get's all detected Fixed Media Drives (fuck Network Drives) 
def dump_drives():
    if MAC_OS in system:
        return macos_dump()
    elif LINUX in system:
        return linux_dump()
    elif WINDOWS in system:
        return windows_dump()
    else:
        logging.critical(INDIE_CRITICAL)
        return None

# Co-Master Function that returns the info of a inputted drive.
# Platform Agnostic
def dump_drive(drive_path):
    try:
        if path.ismount(drive_path):
            drive_name = path.basename(path.dirname(drive_path)) # Because I'm a lazy bum who doesn't wnat to right a slash preflix stripper function. 
            return (drive_name, get_folder_and_files_total(drive_path), get_disk_info(drive_path))
        else:
            logging.warning('%s is not a valid path' % drive_path)
    except Exception:
        logging.critical(INDIE_CRITICAL)
    return None