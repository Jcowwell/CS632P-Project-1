# NOTE: - To Handle Drive Info Logic For -t and --typ arguments
# Author: - Le Zhou

import logging
import platform
from os import listdir, walk, path
from drive_dump import get_system_drives
from helper import get_file_size, get_file_type
from constants import MAC_OS, MACOS_CRITICAL, MACOS_DETECTED, WINDOWS, WINDOWS_CRITICAL, WINDOWS_DETECTED, LINUX, LINUX_DETECTED, INDIE_CRITICAL, ALL 

# NOTE: - LOG
logging.debug('Logging in file_type_dump.py')

# NOTE: - To get the current Operating System this program is being executed on
system = platform.system()

# SECTION: - Logic Functions

# NOTE: - Returns a tuples consiting of two dicts holding file types count and file sizes counts in the following structure: (type_dict, size_dict). Has optional prameter to accept different file types
def get_file_type_details(file, type_dict, size_dict, _type=ALL):
    
    if not path.islink(file):
        type = get_file_type(file)
        if _type == ALL:
            if not type:
                type_dict.setdefault("None", 0)
                type_dict["None"] += 1
                size_dict.setdefault("None", 0)
                size_dict["None"] += get_file_size(file)
            else:
                type_dict.setdefault(type, 0)
                type_dict[type] += 1
                size_dict.setdefault(type, 0)
                size_dict[type] += get_file_size(file)
        else:
            if type == _type:
                type_dict.setdefault(type, 0)
                type_dict[type] += 1
                size_dict.setdefault(type, 0)
                size_dict[type] += get_file_size(file)

    return type_dict, size_dict

# NOTE: - Returns a tuples consiting of two dicts holding file types count and file sizes counts of a drive in the following structure: (type_dict, size_dict). Has optional prameter to accept different file types
def get_file_types_and_size(drive, _type=ALL):
    type_dict = {}
    size_dict = {}
    try:
        for pathnames, _, filenames in walk(drive):
            for file in filenames:
                try:
                    if _type == ALL:
                        get_file_type_details(path.join(pathnames,file), type_dict, size_dict)
                    else:
                        get_file_type_details(path.join(pathnames,file), type_dict, size_dict, _type)
                except PermissionError:
                    logging.warning('Do Not have Permission to Access %s file' % file)
                    continue
                except FileNotFoundError:
                    logging.warning('%s file not found' % file)
                    continue
                except OSError:
                    logging.warning('%s file is waaay too deep in the OS System. I do not think we should be here...' % file)
                    continue
        return type_dict, size_dict
    except Exception as e:
        logging.critical("Cannot get count and size of file types because: %s" % str(e))
    return None

# SECTION: - System Functions

# NOTE: - For MacOS and Darwin Based Systems. Reads all drives in /Volumes. Returns a tuples consiting of two dicts holding file types count and file sizes counts of a drive in the following structure: [(type_dict, size_dict)]| None. Has optional prameter to accept different file types
def macos_dump(type=ALL):
    logging.debug(MACOS_DETECTED)
    file_types = []
    try: 
        for drive in listdir('/Volumes/'):
            logging.debug("Beginning File Type Dumping of: %s" % drive)
            file_types.append(get_file_types_and_size(('/Volumes/' + drive), type))
        return file_types
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (MACOS_CRITICAL, str(e)))
    return None

# NOTE: - For Linux Based Systems
# TODO: - Implemented Linux Support
def linux_dump(type=ALL):
    logging.debug(LINUX_DETECTED)
    return None

# NOTE: - For Windows Based Systems. Get's all detected Fixed Media Drives (fuck Network Drives). Returns a tuples consiting of two dicts holding file types count and file sizes counts of a drive in the following structure: [(type_dict, size_dict)]| None. Has optional prameter to accept different file types
def windows_dump(type=ALL):
    logging.debug(WINDOWS_DETECTED)
    file_types = []
    try:
        drives = get_system_drives()
        if drives is None:
            logging.critical(WINDOWS_CRITICAL)
            return None
        else:
            for drive in drives:
                logging.debug("Beginning File Type Dumping of: %s" % drive)
                file_types.append(get_file_types_and_size(drive,type))
            return file_types
    except Exception as e: 
        logging.critical("%s due to the follwoing error: %s" % (WINDOWS_CRITICAL, str(e)))
    return None

# SECTION: - Driver Functions

# NOTE: - Driver Function inovked by -t args that returns info of all of a system's drives's files types. Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
def dump_file_types(type=ALL):
    if MAC_OS in system:
        return macos_dump(type)
    elif LINUX in system:
        return linux_dump(type)
    elif WINDOWS in system:
        return windows_dump(type)
    else:
        logging.critical(INDIE_CRITICAL)
    return None

# NOTE: - Driver Function inovked by --typ args that returns info of all of a file types. Returns a lists of tuples consiting of a files's size, type, and modify date in the following structure: [(filename, file_size, file_type, file_modify_time)] | None
def dump_file_type(type):
    if type is None:
        logging.critical("%s is an invalid File Type" % type)
        return None
    return dump_file_types(type)