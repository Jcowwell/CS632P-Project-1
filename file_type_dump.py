from os import listdir, walk, path
from helper import format_size
from drive_dump import get_system_drives
from constants import *   
import logging
import platform

system = platform.system()

logging.debug('Logging in file_type_dump.py')

def get_file_size(file):
    '''
    This is used to get the size (byte) of 
    the file in a specific path
    '''

    return path.getsize(file)

def get_file_type(file):
    '''
    This is used to get the type of 
    the file in a specific path
    '''

    return path.splitext(file)[1]



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

def get_file_types_and_size(drive, _type=ALL):
    type_dict = {}
    size_dict = {}
    try:
        for pathnames, _, _files in walk(drive):
            for file in _files:
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
    

def macos_dump(type=ALL):
    logging.debug(MACOS_DETECTED)
    file_types = []
    try: 
        for drive in listdir('/Volumes/'):
            logging.debug("Beginning File Type Dumping of: %s" % drive)
            file_types.append(get_file_types_and_size(('/Volumes/' + drive), type))
        return file_types
    except Exception:
        logging.critical(MACOS_CRITICAL)
    return None

def linux_dump(type=ALL):
    logging.debug(LINUX_DETECTED)
    return None

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
    except Exception:
        logging.critical(WINDOWS_CRITICAL)
    return None

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

def dump_file_type(type):
    if type is None:
        logging.critical("%s is an invalid File Type" % type)
        return None
    return dump_file_types(type)