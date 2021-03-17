# PURP: - TO HANLDE INFO LEVEL LOGGING MESSAGES 

import logging
from helper import format_size

logging.debug('Logging in format.py')

# For -d and -drv arguments
def log_drive_info(drive_name, num_of_files_and_dirs, storage):
    # decouple varibles from touples.
    num_of_files, num_of_dirs = num_of_files_and_dirs
    allocated, used, free = storage
    # Log Drive Info
    logging.debug('Logging Drive Dump')
    logging.info('Drive name / letter: %s' % drive_name)
    logging.info('Total number of directories: %s' % f'{num_of_dirs:,}')
    logging.info('Total number of files: %s' % f'{num_of_files:,}')
    logging.info('Total allocated: %s' % format_size(allocated))
    logging.info('Total used: %s' % format_size(used))
    logging.info('Total free storage: %s' % format_size(free))

def log_drive(drive):
    drive_name, num_of_files_and_dirs, storage = drive
    log_drive_info(drive_name, num_of_files_and_dirs, storage)

def log_drives(drives):
    for drive in drives:
        log_drive(drive)

# For -l -fld arguments
    
#Log Drive Info
def log_folder_info(folder_name, num_of_files, used):
    logging.info('Folder Name: %s' % folder_name)
    logging.info('Total number of files: %s' % f'{num_of_files:,}')
    logging.info("Total amount of space used: %s" %  format_size(used))

def log_total_folder_info(total_used):
    logging.debug('Logging sum of all folders')
    logging.info('Total space used for all folders: %s' % format_size(total_used))

def log_folder(folder):
    logging.debug('Logging Folder Dump')
    folder_name, num_of_files, used, _ = folder
    log_folder_info(folder_name, num_of_files, used) # Implement function

def log_folders(folders):
    logging.debug('Logging Folder Dump')
    directories, total_storage = folders
    for folder in directories:
        folder_name, num_of_files, used = folder
        log_folder_info(folder_name, num_of_files, used) # Implement function
    log_total_folder_info(total_storage) # Implement function

# For -f and -fil arguments

def log_files_info(file_name, file_type, file_size, file_date):
    logging.debug('Logging File Dump')
    logging.info('File Name: %s' % file_name)
    logging.info('File Type: %s' % file_type)
    logging.info("File size: %s" % format_size(file_size))
    logging.info("File Date/Time: %s" % file_date)

def log_file(file):
    file_name, file_type, file_size, file_date = file
    log_files_info(file_name, file_type, file_size, file_date)

def log_files(files):
    for file in files:
        log_file(file)

def log_file_type_info(file_type, num_of_files, total_storage):
    logging.debug('Logging File Type Dump')
    logging.info('File Type: %s' % file_type)
    logging.info('Total # of files: %s' % num_of_files)
    logging.info("Total storage: %s" % format_size(total_storage))

# Tuples of Dictonary
def log_file_type(file_type):
    print(file_type)
    type, size = file_type
    for _type in type.keys():
        log_file_type_info(_type, type[_type], size[_type])

# Lists of Tuples of Dictonary
def log_file_types(file_types):
    for file_type in file_types:
        log_file_type(file_type)
    




    
    
    

