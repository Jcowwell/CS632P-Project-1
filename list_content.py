# PURP: - TO HANLDE INITAL LOGGING AND ARGS LOGIC. 
import logging
import argparse
from drive_dump import dump_drives, dump_drive
from folder_dump import dump_folder, dump_folders
from info_logger import log_drive_info, log_folders, log_folder
from constants import D, DRV, L, FLD, F, FIL, T, TYP, LOG_FORMAT, LOG_DATE_FORMAT


# MARK:- Logger Initilized
logging.basicConfig(filename='dump.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logging.debug("Logging Initilized")

# MARK:- Set up Argparse paramaeters
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

args = parser.parse_args(args=['-d', 'D'])

# MARK:- Begin Args Parameters Handeling
logging.debug("Beginning Args Handeling...")
# MARK:- -d args
if args.d:
    logging.debug('-d argument was passed')
    logging.debug("Dumping Local Computer Drives info")

    drives = dump_drives()
    if drives is None:
        logging.critical('Program was unable to process request')
        logging.error("Could Not Dump Drive Info")
    else: 
        for drive in drives:
            drive_name, num_of_files_and_dirs, storage = drive
            log_drive_info(drive_name, num_of_files_and_dirs, storage)
       

# MARK:- -drv args
if args.drv:
    logging.debug('-drv argument was passed')
    logging.debug("Dumping info of %s Drive" % args.drv)
    drive = dump_drive(args.drv)
    if drive is None:
        logging.critical('Program was unable to process %s path' % args.drv)
    else:
        drive_name, num_of_files_and_dirs, storage = drive
        log_drive_info(drive_name, num_of_files_and_dirs, storage)

# MARK:- -l args
if args.l:
    logging.debug('-l argument was passed')
    logging.debug('Dumping the info of %s drive' % args.l )

    folders = dump_folders(args.l)
    if folders is None:
        logging.critical("The program was unable to obtain folder info ")
        logging.error("Could Not Dump folder info")
    else:
        log_folders(folders)

# MARK:- --fld args
if args.fld:
    logging.debug('--fld argument was passed')
    logging.debug('Dumping the info of %s folder' % args.fld)

    folder = dump_folder(args.fld)
    if folder is None:
        logging.critical('The program was unable to obtain info from folder')
        logging.error('Could not dump folder info')   
    else:
         log_folder(folder)

# MARK:- -f args
if args.f:
    logging.debug('-f argument was passed')

# MARK:- --fil args
if args.fil:
    logging.debug('--fil argument was passed')

# MARK:- -t args
if args.t:
    logging.debug('-t argument was passed')

# MARK:- -typ args
if args.typ:
    logging.debug('--typ argument was passed')