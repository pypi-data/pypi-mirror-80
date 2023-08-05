import logging
import datetime
import os

# LOGGING
def create_logger(logging_level=None, logger_name=None, logging_format = None,log_to_console=True,log_file_folder=None,save_new_day_in_own_folder=False):
    '''Does the setup for the log and the config file'''
    # Setup logging
    if logger_name is None:
        logger_name = __name__

    if logging_level is None:
        logging_level = logging.INFO

    if logging_format is None:
        logging_format = logging.Formatter(fmt='%(asctime)s.%(msecs)03d|%(funcName)s|%(levelname)s|%(message)s',
                                           datefmt='%d-%b-%y %H:%M:%S')
    if log_file_folder is None:
        log_file_folder = 'logs'

    if save_new_day_in_own_folder:
        log_file_folder = os.path.join(log_file_folder,f'{datetime.datetime.today().strftime("%Y-%m-%d")}')

    # make sure the dir that the log file is to be placed in does exist
    if not os.path.exists(log_file_folder):
        os.makedirs(log_file_folder)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    handler = logging.FileHandler(os.path.join(log_file_folder,f'{logger_name}.log'))
    logger.addHandler(handler)
    handler.setFormatter(logging_format)
    if log_to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

    logger.debug(f'Logger "{logger_name}" created')

    if not log_to_console:
        logger.propagate = False

    return logger

def setup_global_logging(logging_level=None, logger_name =None, logging_format=None,log_file_folder=None):
    if logging_level is None:
        logging_level = logging.INFO

    if logger_name is None:
        logger_name = 'main_log_file.log'

    if log_file_folder is not None:
        log_file_folder = 'logs'

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    try:
        logging.basicConfig(format='%(asctime)s.%(msecs)03d|%(filename)s|%(funcName)s|%(levelname)s|%(message)s',
                            datefmt='%d-%b-%y %H:%M:%S',
                            level=logging_level, filename=os.path.join(log_file_folder,logger_name))
    except FileNotFoundError:
        # if it cannot find the log it will create the log file and folder
        log_file_folder = os.path.join(os.getcwd(), 'logs')
        if not os.path.isdir(log_file_folder):
            os.makedirs(log_file_folder)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d|%(filename)s|%(funcName)s|%(levelname)s|%(message)s',
                            datefmt='%d-%b-%y %H:%M:%S',
                            level=logging_level, filename=os.path.join(log_file_folder,logger_name))

    logging.propagate=False
    logging.info('Created global logger')