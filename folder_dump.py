from os import listdir, walk, path, scandir
from drive_dump import get_disk_info  
from helper import format_size
import logging
import platform
import shutil
import ctypes
from constants import *


logging.debug("Logging in folder_dump.py")

# Return a tuple (dirname,num_of_files)
def get_folder_info(folder):
    files = 0
    try:
        for file in scandir(folder):
            if path.isfile(file):
                files+=1
    except PermissionError:
        logging.error("Does not have permission to access data")
    return (folder,files)

# Should return a lists of tuples (dirname, # of files)
def get_folder_and_num_of_files(drive):
    folders = []
    try:
        for pathnames, dirnames, _ in walk(drive):
            for folder in dirnames:
                folders.append(get_folder_info(path.join(pathnames,folder)))
            break
    except Exception as e:
        logging.critical("Cannot get count of drive's folder files and folders because: %s" % str(e))
        return None # empty lists I work out null handling

    return folders

# returns a tuple (dirname, num_of_files, (allocated, used, free))
def get_folder_size(folder):
    dirnames, num_of_files = folder
    folder += (get_disk_info(folder),)
    return folder

# -l master method
    # Checking if valid path if not return none
    # if valid get info in a try catch
    # if an excpetion occurs return none
def dump_folders(drive):
    if os.path.ismount(drive):
        #drive_name = path.basename(path.dirname(drive))
        try:
            folders = []
            files = get_folder_and_num_of_files(drive)
            if files is None:
                logging.critical('The program was unable to get folders and number of directories')
                return None
            else:
                for folder in files:
                    dirnames, num_of_files = folder
                    folder += (get_disk_info(drive + dirnames),)
                    folders.append(folder)
                    tup = (folders, get_disk_info(drive))
                return tup
        except Exception:
            logging.critical(INDIE_CRITICAL)
            return None
    else:
        return None


# --fld master method
    # Checking if valid path if not return none
    # if valid get info in a try catch
    # if an excpetion occurs return none
def dump_folder(folder):
    if os.path.isdir(folder):
        try:
            
            get_folder =  get_folder_info(folder)
            get_folder += (get_disk_info(folder),)
            return (get_folder)
            

        except Exception:
            logging.critical(INDIE_CRITICAL)
            return None
    else:
        return None
    return



