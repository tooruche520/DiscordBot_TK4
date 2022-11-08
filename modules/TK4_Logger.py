import os
import time
import logging as log

def TK4_logger():
    log_dir = os.getcwd() + '/logs/'
    # log_path = os.getcwd() + os.sep + log_dir
    folder = os.path.exists(log_dir)
    if not folder:
        os.makedirs(log_dir)
        # log.info(f'Create Folder "LogFiles" ')
    # else:
        # log.info(f'The Folder "LogFiles" are already have')

    logger = log.getLogger()
    logger.setLevel(log.INFO)
    formatter = log.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)

    ch = log.StreamHandler()
    ch.setFormatter(formatter)

    log_filename = log_dir + time.strftime("%Y-%m-%d") + '_log.txt'
    fh = log.FileHandler(log_filename, encoding='utf-8',)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    log.info('TK4_logger called!')

    # return log

# TK4_logger()
