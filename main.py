import os
import time
import argparse
import logging

# basic config
logging.basicConfig(filename="log.txt",
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger=logging.getLogger(__name__)

#　set level
logger.setLevel(logging.INFO)


def get_file_size(file):
    '''
    This is used to get the size (byte) of 
    the file in a specific path
    '''

    return os.path.getsize(file)


def timestamp_to_date(t):
    '''
    get the time and format it
    :return:
    '''

    t_s = time.localtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S',t_s)


def get_file_modify_time(file):
    '''
    get the time of last modification

    '''

    return os.path.getmtime(file)


def handle_f(root):
    '''
    -f function implement

    '''
    # get all the files and dirs in the specific path
    dir_or_files = os.listdir(root)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root, dir_file)

        # if the path is a dir / folder
        if os.path.isdir(dir_file_path):
            # keep looping to the get the non-folder(file) path
            handle_f(dir_file_path)
        # print and log the file info
        else:
            suffix = dir_file_path.split('.')[-1]
            file_size = get_file_size(os.path.join(root, dir_file_path))
            file_modify_time = get_file_modify_time(os.path.join(root, dir_file_path))
            file_date = timestamp_to_date(file_modify_time)
            print('filename: {}, suffix: {}, filesize: {} Byte, modify_time: {}, date: {}'.format(dir_file_path, suffix, file_size, file_modify_time, file_date))
            logger.info('filename: {}, suffix: {}, filesize: {} Byte, modify_time: {}, date: {}'.format(dir_file_path, suffix, file_size, file_modify_time, file_date))


def handle_fil(f):
    '''
    this part is for -fil function implementation

    '''

    # handle and record errors 
    if not os.path.exists(f):
        logger.warning('{} is not exists.'.format(f))
        print('{} is not exists.'.format(f))
        return

    if not os.path.isfile(f):
        logger.error('{} is not a file.'.format(f))
        print('{} is not a file.'.format(f))
        return
    # if the file exists and error free, print the information, the similar to  -f
    else:
        suffix = f.split('.')[-1]
        file_size = get_file_size(f)
        file_modify_time = get_file_modify_time(f)
        file_date = timestamp_to_date(file_modify_time)
        print('filename: {}, suffix: {}, filesize: {} Byte, modify_time: {}, date: {}'.format(f, suffix, file_size, file_modify_time, file_date))
        logger.info('filename: {}, suffix: {}, filesize: {} Byte, modify_time: {}, date: {}'.format(f, suffix, file_size, file_modify_time, file_date))

# initialize parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-fil', help='for file.')
    parser.add_argument('-f', help='for dir.')

    opt = parser.parse_args()

    if opt.fil:
        handle_fil(opt.fil)

    if opt.f:
        handle_f(opt.f)