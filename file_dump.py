from os import listdir, walk, path
from helper import format_size
from drive_dump import get_system_drives
from constants import *   
import time
import logging
import platform

system = platform.system()

# basic config
logging.debug('Logging in format.py')

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

def get_file_modify_time(file):
    '''
    get the time of last modification

    '''

    return time.strftime(LOG_DATE_FORMAT, time.gmtime(path.getmtime(file)))

def get_file_details(file):
    file_name = path.basename(file)
    try:
        file_size = format_size((get_file_size(file)))
        file_type = get_file_type(file)
        file_modify_time = get_file_modify_time(file)
        return (file_name, file_size, file_type, file_modify_time)
    except PermissionError:
        logging.warning('Do Not have Permission to Access %s file' % file_name)
    except FileNotFoundError:
        logging.warning('%s file not found' % file_name)
    except OSError:
        logging.warning('%s file is waaay too deep in the OS System. I do not think we should be here...' % file_name)
    return (file_name, None, None, None)

def get_files(drive):
    files = []
    try:
        for pathnames, _, _files in walk(drive):
            for file in _files:
                file_path = path.join(pathnames,file)
                if not path.islink(file_path):
                    files.append(get_file_details(file_path))
        return files
        
    except Exception as e:
        logging.critical("Cannot get count of drive's folder files because: %s" % str(e))
    return None

def macos_dump():
    logging.debug(MACOS_DETECTED)
    files = []
    try: 
        for drive in listdir('/Volumes/'):
            logging.debug("Beginning Info Dumping of: %s" % drive)
            files.extend(get_files('/Volumes/' + drive))
        return files
    except Exception:
        logging.critical(MACOS_CRITICAL)
    return None

def linux_dump():
    logging.debug(LINUX_DETECTED)
    return None

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
    except Exception:
        logging.critical(WINDOWS_CRITICAL)
    return None

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

def dump_file(file):
    try:
        if path.isfile(file):
            return get_file_details(file)
        else:
            logging.warning('%s is not a valid file' % file)
    except Exception:
        logging.critical(INDIE_CRITICAL)
    return None