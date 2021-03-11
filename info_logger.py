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
    logging.info('Total allocated: %s GiB' % f'{allocated:,}')
    logging.info('Total used: %s GiB' % f'{used:,}')
    logging.info('Total free storage: %s GiB' % f'{free:,}')


