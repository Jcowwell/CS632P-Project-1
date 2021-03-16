# PURP: - TO HANLDE INFO LEVEL LOGGING MESSAGES 

import logging

logging.debug('Logging in format.py')

def log_drive_info(drive_name, num_of_files_and_dirs, storage):
    # decouple varibles from touples.
    num_of_files, num_of_dirs = num_of_files_and_dirs
    allocated, used, free = storage
    # Log Drive Info
    logging.debug('Logging Drive Dump')
    logging.info('Drive name / letter: %s' % drive_name)
    logging.info('Total number of directories: %s' % f'{num_of_dirs:,}')
    logging.info('Total number of files: %s' % f'{num_of_files:,}')
    logging.info('Total allocated: %s' % allocated)
    logging.info('Total used: %s' % used)
    logging.info('Total free storage: %s' % free)


def log_folders(folders):
    directories, total_storage = folders
    _, total_used , _ = total_storage
    for folder in directories:
        folder_name, num_of_files, storage = folder
        _, used , _ = storage
        log_folder_info(folder_name, num_of_files, used) # Implement function
    log_total_folder_info(total_used) # Implement function
    
#Log Drive Info
def log_folder_info(folder_name, num_of_files, used):
    logging.debug('Logging Folder Dump')
    logging.info('Folder Name: %s' % folder_name)
    logging.info('Total number of files: %s' % f '{num_of_files:,}')
    logging.info("Total amount of space used: %s" % f '{used}')

def log_total_folder_info(total_used):
    logging.debug('Logging sum of all folders')
    logging.info('Total space used for all folders: %s' % f '{total_used}')

def log_folder(folder):
    dirname, total_storage = folders
    _, total_used, _ = total_storage


    log_folder_info(dirname, num_of_files, total_used) # Implement function
    
    
    

