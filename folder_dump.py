# NOTE: - To Handle Drive Info Logic For -f and --fld arguments
# Author: - Calvin Cheung

import logging
from os import walk, path
from helper import get_file_size
from drive_dump import get_disk_info  


# NOTE: - LOG
logging.debug("Logging in folder_dump.py")

# SECTION: - Logic Functions

# NOTE: - Returns a tuple of a foldler's file count and size in the following stucture: (folder,num_of_files,size)
def get_folder_info(folder):
    files = 0
    size = 0
    for pathnames, _, filenames in walk(folder):
        try:
            for file in filenames:
                filepath = path.join(pathnames, file)
                # skip if it is symbolic link cause fuck symbolic links
                if not path.islink(filepath):
                    files += 1
                    size += get_file_size(filepath)
        except PermissionError:
            logging.error("Does not have permission to access %s" % file)
            continue
        except FileNotFoundError:
            logging.warning('%s folder not found' % file)
            continue
        except OSError:
            logging.warning('%s folder is waaay too deep in the OS System. I do not think we should be here...' % file)
            continue

    return (folder,files,size)

# NOTE: - Returns a lists of tuples of a foldler's file count and size in the following stucture: (folder,num_of_files,size) | None
def get_folder_data(drive):
    folders = []
    try:
        for pathnames, dirnames, _ in walk(drive):
            for folder in dirnames:
                try:
                    folder_path = path.join(pathnames,folder)
                    if not path.islink(folder_path):
                        folders.append(get_folder_info(folder_path))
                except PermissionError:
                    logging.error("Does not have permission to access %s" % folder)
                    continue
                except FileNotFoundError:
                    logging.warning('%s folder not found' % folder)
                    continue
                except OSError:
                    logging.warning('%s folder is waaay too deep in the OS System. I do not think we should be here...' % folder)
                    continue
            break
        return folders
    except Exception as e:
        logging.critical("Cannot get count of drive's folder files and folders because: %s" % str(e))
    return None 

# NOTE: - Returns the sum of all the storage
def sum_folders(folders):
    sum = 0
    for folder in folders:
        size = folder[2]
        sum += size
    return sum

# SECTION: - Driver Functions

# NOTE: - Driver Function inovked by -l args that returns info of all of a drives' folders. Returns a lists of tuples in the following stucture: ((folder,num_of_files,size),sum_storage) | None
def dump_folders(drive):
    # Checking if is a valid drive/mount for cross-platform
    if path.ismount(drive):
        try:
            folders = get_folder_data(drive) # (folder,num_of_files,size) | None
            if folders is None:
                logging.critical('The program was unable to get folders and number of directories')
            else:
                return (folders, sum_folders(folders)) 
        except Exception as e:
            logging.critical("Cannot get %s drive's folder info due to: %s" % (drive, str(e)))
    else:
         logging.warning("%s is not a valid drive", drive)
    return None

# NOTE: - Driver Function inovked by -fld args that returns info of a folder. Returns a tuple in the following stucture: ((folder,num_of_files,size),sum_storage) | None
def dump_folder(folder):
    # Checking if is a valid folder for cross-platform
    if path.isdir(folder):
        try:
            get_folder =  get_folder_info(folder) # (folder,num_of_files,size)
            get_folder += (get_disk_info(folder),) # (folder,num_of_files,size, sum_storage)
            return get_folder
        except Exception as e: 
            logging.critical("Cannot get %s folder info due to: %s" % (folder, str(e)))
    else:
        logging.warning("%s is not a valid folder", folder)
    return None



