# NOTE: - Helper Functions to use throughout the program
import time
import logging
from os import path
from constants import COMP_ERROR, LOG_DATE_FORMAT

# SECTION: - Helper Functions

# NOTE: - Formats Bytes size into GB,MB, & kb
def format_size(num):
    if num is None: return "0 B"
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, "B")
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', "B")

# NOTE: - Returns the size (byte) of a file
def get_file_size(file):

    return path.getsize(file)

# NOTE: - Returns the file type of a file by it's extension
def get_file_type(file):

    return path.splitext(file)[1]

# NOTE: - Returns the modified date of  file
def get_file_modify_time(file):
 
    return time.strftime(LOG_DATE_FORMAT, time.gmtime(path.getmtime(file)))