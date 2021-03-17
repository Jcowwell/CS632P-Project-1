# NOTE: - To Handle Drive Info Logic For -d and --drv arguments
# Author: - Jevon Cowell
from os import listdir, walk, path
from constants import DRIVE_FIXED, MAC_OS, MACOS_CRITICAL, MACOS_DETECTED, WINDOWS, WINDOWS_CRITICAL, WINDOWS_DETECTED, LINUX, LINUX_DETECTED, INDIE_CRITICAL   
import logging
import platform
import shutil
import ctypes

# NOTE: - LOG
logging.debug('Logging in drive_dump.py')

# NOTE: - To get the current Operating System this program is being executed on
system = platform.system()

# SECTION: - Logic Functions

# NOTE: - Returns a list of tuples mapping drive letters to drive types for Windows Systems in the following structure: [(drive_letter, drive_type)]| [] . Adopted From StackOverFLow Post: https://stackoverflow.com/a/17030773/6427171
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

# NOTE: - Returns list of system drives in the following structure: [(drive_letter, drive_type)] | None
def get_system_drives():
    try:
        drive_info = get_drive_info()
    except Exception as e: 
        logging.critical("Cannot get system's drives due to the follwoing error: %s" % str(e))
        return None
    return [drive_letter for drive_letter, drive_type in drive_info if drive_type == DRIVE_FIXED]

# NOTE: - Returns a tuple of a disk's total files and folders count in the following structure: (files, folder) | (None, None)
def get_folder_and_files_total(directory):
    
    files = folders = 0
    try:
        for _, dirnames, filenames in walk(directory):
            files += len(filenames)
            folders += len(dirnames)
    except Exception as e: 
        logging.critical("Cannot get count of drive's files and folders due to: %s", str(e))
        return None, None
    if files < 0:
        logging.error("File count less than 0")
        return None, None
    if folders < 0:
         logging.error("Folder count less than 0")
         return None, None

    return files, folders

# NOTE: - Returns a tuple of a disk's total, used, and free space in the following: strucuture: (total, used, free) | (None, None, None)
def get_disk_info(drive):
    try:
        return shutil.disk_usage(drive)
    except Exception as e: 
        logging.critical("Cannot get drive's storage info due to: %s" % str(e))
    return None, None, None

# SECTION: - System Functions

# NOTE: - For MacOS and Darwin Based Systems. Reads all drives in /Volumes. Returns a lists of tuples in the following stucture: ((drive, (file_counts, folder_counts)), (total, used, free)) | None
def macos_dump():
    logging.debug(MACOS_DETECTED)
    drive_info = []
    try: 
        for drive in listdir('/Volumes'):
            logging.debug("Beginning Info Dumping of: %s" % drive)
            drive_info.append((drive, get_folder_and_files_total('/Volumes/' + drive), get_disk_info('/Volumes/' + drive)))
        return drive_info
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (MACOS_CRITICAL, str(e)))
    return None

# NOTE: - For Linux Based Systems
def linux_dump():
    logging.debug(LINUX_DETECTED)
    return None

# NOTE: - For Windows Based Systems. Get's all detected Fixed Media Drives (fuck Network Drives). Returns a lists of tuples in the following stucture: ((drive, (file_counts, folder_counts)), (total, used, free)) | None
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
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (WINDOWS_CRITICAL, str(e)))
    return None

# SECTION: - Driver Functions

# NOTE: - Driver Function inovked by -d args that returns info of all of a system's drives. Returns a lists of tuples in the following stucture: ((drive, (file_counts, folder_counts)), (total, used, free)) | None
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

# # NOTE: - Driver Function inovked by --drv args that returns info of desired drive in the following strucutre: ((drive, (file_counts, folder_counts)), (total, used, free)) | None
def dump_drive(drive):
    try:
        if path.ismount(drive):
            drive_name = path.basename(path.dirname(drive)) # Because I'm a lazy bum who doesn't wnat to right a slash preflix stripper function. 
            return (drive_name, get_folder_and_files_total(drive), get_disk_info(drive))
        else:
            logging.warning('%s is not a valid drive' % drive)
    except Exception as e: 
        logging.critical("Cannot get %s drive's folder info due to: %s" % (drive, str(e)))
    return None