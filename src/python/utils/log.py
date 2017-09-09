#
#                       o   o                            
#                       8                                
# .oPYo. .oPYo. odYo.  o8P o8 .oPYo. odYo. .oPYo. .oPYo. 
# Yb..   8oooo8 8' `8   8   8 8oooo8 8' `8 8    ' 8oooo8 
#   'Yb. 8.     8   8   8   8 8.     8   8 8    . 8.     
# `YooP' `Yooo' 8   8   8   8 `Yooo' 8   8 `YooP' `Yooo' 
# :.....::.....:..::..::..::..:.....:..::..:.....::.....:
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#   Copyright Yazan Obeidi, 2017
#
#   python.utils.log 
#

import logging
from os import makedirs
from os import path
from os import environ

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

def init_log(name, log_file=None):
    using_temp_logs = False
    if not log_file:
        # Get logging directory from environment variable
        log_dir = environ.get("SENTIENCE_LOG_DIR")
        log_name = "{}_runlog.log".format(name)
        # If no environment variable is set, create temp location
        if not log_dir:
            temp_log_dir = "/tmp/sentience/log"
            path.join(temp_log_dir, log_name)
            using_temp_logs = True
        else:
            log_file = path.join(log_dir, log_name)
    # Create logging directory if it does not exist:
    if not path.exists(path.dirname(log_file)):
        makedirs(path.dirname(log_file))
    # Logging boilerplate
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file, mode='w+')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '\
                                                            '- %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    if using_temp_logs:
        logger.warn("Using temporary logs saved to - {}".format(log_file))
    else:
        logger.debug("Logs saved to - {}".format(log_file))
    return logger