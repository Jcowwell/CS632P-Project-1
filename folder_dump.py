from os import listdir, walk, path
from constants import *   
from helper import format_size
import logging
import platform
import shutil
import ctypes

logging.debug("Logging in folder_dump.py")