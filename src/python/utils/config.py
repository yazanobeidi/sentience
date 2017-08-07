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
#   python.utils.config 
#

from configparser import ConfigParser
from os import path
from os import environ
import glob

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

def init_config(config_dir=None):
    config = ConfigParser(environ)
    # If configuration directory is an ENV variable, fetch it
    if not config_dir:
        config_dir = environ.get("SENTIENCE_CONFIG_DIR")
    else:
        raise Exception("Configuration directory not found {}".format(config_dir))
    # Identify base configuration file:
    main_config_file = path.join(config_dir, "base_config.cfg")
    # Load it first, if it exists
    if path.isfile(main_config_file):
        config.read(main_config_file)
    # Get the other configuration files, anything inside that directory.
    for file in glob.glob(config_dir + '/**/*.cfg', recursive=True):
        # Don't re read the base configuration file
        if file == "base_config.cfg":
            continue
        else:
            config.read(file)
    return config