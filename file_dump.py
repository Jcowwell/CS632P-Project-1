# NOTE: - TO HANDLE DRIVE INFO LOGIC FOR -f and --fil arguments
# Author: - Lang Gong

import logging
import platform
from os import listdir, walk, path
from drive_dump import get_system_drives
from helper import get_file_size, get_file_type, get_file_modify_time
from constants import MAC_OS, MACOS_CRITICAL, MACOS_DETECTED, WINDOWS, WINDOWS_CRITICAL, WINDOWS_DETECTED, LINUX, LINUX_DETECTED, INDIE_CRITICAL   

# NOTE: - LOG
logging.debug('Logging in file_dump.py')

# NOTE: - To get the current Operating System this program is being executed on
system = platform.system()

# SECTION: - Logic Functions

# NOTE: - Returns a tuples consiting of a files's size, type, and modify date in the following structure: (filename, file_size, file_type, file_modify_time) | (filename, None, None, None)
def get_file_details(file):
    filename = path.basename(file)
    try:
        file_size = get_file_size(file)
        file_type = get_file_type(file)
        file_modify_time = get_file_modify_time(file)
        return (filename, file_size, file_type, file_modify_time)
    except PermissionError:
        logging.warning('Do Not have Permission to Access %s file' % filename)
    except FileNotFoundError:
        logging.warning('%s file not found' % filename)
    except OSError:
        logging.warning('%s file is waaay too deep in the OS System. I do not think we should be here...' % filename)
    return (filename, None, None, None)

# NOTE: - Returns a lists of tuples consiting of a ffiles's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
def get_files(drive):
    files = []
    try:
        for pathnames, _, filenames in walk(drive):
            for file in filenames:
                file_path = path.join(pathnames,file)
                if not path.islink(file_path):
                    files.append(get_file_details(file_path))
        return files
    except Exception as e:
        logging.critical("Cannot get count of drive's folder files because: %s" % str(e))
    return None

# SECTION: - System Functions

# NOTE: - For MacOS and Darwin Based Systems. Reads all drives in /Volumes. Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
# REVIEW: - Check if were properly structuring the lists so that each drive is accounted for. 
def macos_dump():
    logging.debug(MACOS_DETECTED)
    files = []
    try: 
        for drive in listdir('/Volumes/'):
            logging.debug("Beginning File Dumping of: %s" % drive)
            files.extend(get_files('/Volumes/' + drive)) 
        return files
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (MACOS_CRITICAL, str(e)))
    return None

# NOTE: - For Linux Based Systems
# TODO: - Implemented Linux Support
def linux_dump():
    logging.debug(LINUX_DETECTED)
    return None

# NOTE: - For Windows Based Systems. Get's all detected Fixed Media Drives (fuck Network Drives). Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
# REVIEW: - Check if were properly structuring the lists so that each drive is accounted for. 
def windows_dump():
    logging.debug(WINDOWS_DETECTED)
    files = []
    try:
        drives = get_system_drives()
        if drives is None:
            logging.critical(WINDOWS_CRITICAL)
            return None
        else:
            for drive in drives:
                logging.debug("Beginning File Dumping of: %s" % drive)
                files.extend(get_files(drive)) 
            return files
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (WINDOWS_CRITICAL, str(e)))
    return None

# SECTION: - Driver Functions

# NOTE: - Driver Function inovked by -f args that returns info of all of a system's drives's files. Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
def dump_files():
    if MAC_OS in system:
        return macos_dump()
    elif LINUX in system:
        return linux_dump()
    elif WINDOWS in system:
        return windows_dump()
    else:
        logging.critical(INDIE_CRITICAL)
    return None

# NOTE: - Driver Function inovked by -fil args that returns info of a files. Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: (filename, file_size, file_type, file_modify_time) | None
def dump_file(file):
    try:
        if path.isfile(file):
            logging.debug("Beginning Dumping of: %s" % file)
            return get_file_details(file)
        else:
            logging.warning('%s is not a valid file' % file)
    except Exception as e: 
        logging.critical("Cannot get %s file info due to: %s" % (file, str(e)))
    return None