# NOTE: - To Handle Initial Logging And Args Logic
# REVIEW: - Check if Windows Systems are 100% compatible

import logging
from constants import D, DRV, L, FLD, F, FIL, T, TYP, LOG_FORMAT, LOG_DATE_FORMAT

# NOTE: - Logger Initilized
logging.basicConfig(filename='dump.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logging.debug("Logging Initilized")

import argparse
from drive_dump import dump_drives, dump_drive
from folder_dump import dump_folder, dump_folders
from file_dump import dump_files, dump_file
from file_type_dump import dump_file_types, dump_file_type
from info_logger import log_drives, log_drive, log_folders, log_folder, log_files, log_file, log_file_types

# SECTION ARGS Initilization
# NOTE: - Set up Argparse paramaeters
parser = argparse.ArgumentParser()
parser.add_argument(D, help='list all the drives of the machine with additional info')
parser.add_argument(DRV, help='list additional info of single drive')

parser.add_argument(L, help='list all the folders of the machine with additional info:')
parser.add_argument(FLD, help='list additional info of single folder')

parser.add_argument(F, help='list all the files of the machine with additional info')
parser.add_argument(FIL, help='list additional info of single file')

parser.add_argument(T, help='list all the types of files of the machine with additional info')
parser.add_argument(TYP, help='list additional info of type of single file')
logging.debug("Args Added")

#NOTE: -  In-Code arg passing (For Testing)
args = parser.parse_args(args=['-t', 'T'])

# SECTION ARGS Handeling
# NOTE: - Beginning Args Parameters Handeling
logging.debug("Beginning Args Handeling...")

# SECTION -d and --drv
# NOTE: - -d args
if args.d:
    logging.debug('-d argument was passed')
    logging.debug("Dumping Local Computer Drives info")

    drives = dump_drives()
    if drives is None:
        logging.critical('Program was unable to process request')
        logging.error("Could Not Dump Drive Info")
    else: 
        log_drives(drives)
       

# NOTE: - -drv args
if args.drv:
    logging.debug('-drv argument was passed')
    logging.debug("Dumping info of %s Drive" % args.drv)
    drive = dump_drive(args.drv)
    if drive is None:
        logging.critical('Program was unable to process %s path' % args.drv)
    else:
        log_drive(drive)

# SECTION -l and --fld
# NOTE: - -l args
if args.l:
    logging.debug('-l argument was passed')
    logging.debug('Dumping the info of %s drive' % args.l )

    folders = dump_folders(args.l)
    if folders is None:
        logging.critical("The program was unable to obtain folder info ")
        logging.error("Could Not Dump folder info")
    else:
        log_folders(folders)

# NOTE: - --fld args
if args.fld:
    logging.debug('--fld argument was passed')
    logging.debug('Dumping the info of %s folder' % args.fld)

    folder = dump_folder(args.fld)
    if folder is None:
        logging.critical('The program was unable to obtain info from %s' % args.fld)  
    else:
         log_folder(folder)

# SECTION -f and --fil
# NOTE: - -f args
if args.f:
    logging.debug('-f argument was passed')
    logging.debug("Dumping the info of this machine's files...Hold your butcheeks")
    files = dump_files()
    if files is None:
        logging.critical('The program was unable to obtain files info from this machine')
        logging.error("Could not dump this machine's file's info") 
    else:
        log_files(files)

# NOTE: - --fil args
if args.fil:
    logging.debug('--fil argument was passed')
    logging.debug('Dumping the info of %s' % args.fil)
    file = dump_file(args.fil)
    if file is None:
        logging.critical('The program was unable to obtain info from %s' % args.fil)
    else:
        log_file(file)
        
# SECTION -t and --typ
# NOTE: - -t args
if args.t:
    logging.debug('-t argument was passed')
    logging.debug("list all type and the total storage")
    file_types = dump_file_types()
    if file_types is None:
        logging.critical('The program was unable to obtain file types info from this machine')
        logging.error("Could not dump this machine's file types info") 
    else:
        log_file_types(file_types)

# NOTE: - -typ args
if args.typ:
    logging.debug('--typ argument was passed')
    logging.debug("list all type and the total storage")
    file_types = dump_file_type(args.typ)
    if file_types is None:
        logging.critical('The program was unable to obtain info from %s' % args.fil) 
    else:
        log_file_types(file_types)
