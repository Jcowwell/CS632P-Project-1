from os import listdir, walk, path, scandir
from drive_dump import get_disk_info  
from helper import format_size
import logging
from constants import *


logging.debug("Logging in folder_dump.py")

# Return a tuple (dirname,num_of_files)
def get_folder_info(folder):
    files = 0
    total_size = 0
    try:
        for dirpath, dirnames, filenames in walk(folder):
            for f in filenames:
                fp = path.join(dirpath, f)
                # skip if it is symbolic link
                if not path.islink(fp):
                    files += 1
                    total_size += path.getsize(fp)
    except PermissionError:
        logging.error("Does not have permission to access %s" % folder)
    except FileNotFoundError:
        logging.warning('%s folder not found' % folder)
    except OSError:
        logging.warning('%s folder is waaay too deep in the OS System. I do not think we should be here...' % folder)
    
    return (folder,files,total_size)

# Should return a lists of tuples (dirname, # of files, total_size)
def get_folder_data(drive):
    folders = []
    try:
        for pathnames, dirnames, _ in walk(drive):
            for folder in dirnames:
                folder_path = path.join(pathnames,folder)
                if not path.islink(folder_path):
                    folders.append(get_folder_info(folder_path))
            break
    except Exception as e:
        logging.critical("Cannot get count of drive's folder files and folders because: %s" % str(e))
        return None # empty lists I work out null handling

    return folders

def sum_folders(folders):
    sum = 0
    for folder in folders:
        size = folder[2]
        sum += size
    return sum

# returns a tuple ((dirname, num_of_files,total_size), sum_of_all_folder_size)

# -l master method
    # Checking if valid path if not return none
    # if valid get info in a try catch
    # if an excpetion occurs return none
def dump_folders(drive):
    if path.ismount(drive):
        #drive_name = path.basename(path.dirname(drive))
        try:
            
            folders = get_folder_data(drive)
            if folders is None:
                logging.critical('The program was unable to get folders and number of directories')
                return None
            else:
                return (folders, sum_folders(folders))
        except Exception as e:
            logging.critical(INDIE_CRITICAL)
            return None
    else:
        return None


# --fld master method
    # returns ((dirname, num_of_files),(allocated, used, free))
def dump_folder(folder):
    if path.isdir(folder):
        try:
            
            get_folder =  get_folder_info(folder)
            get_folder += (get_disk_info(folder),)
            return get_folder
            

        except Exception:
            logging.critical(INDIE_CRITICAL)
            return None
    else:
        return None



