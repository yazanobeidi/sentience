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
#   python.learning.learn - single interface for learning
#

from src.python.utils.log import init_log
from src.python.utils.config import init_config
from src.python.learning.models import Model

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

class Trainer(object):
    """Consumes data/dataset in streamable or batch format
        and trains a single model in the available catalogue.
    """
    def __init__(self, log, config, model_handle, model_schema):
        """:params:
            model_handle: a model object, i.e. a RandomForest clf handler
            model_schema: reference to the library for that model, i.e. sklearn
        """
        self.log = log
        self.config = config
        self.model = model_handle
        self.schema = model_schema

    def train(self):
        pass

    @property
    def score(self):
        pass


if __name__ = '__main__':
    log = init_log()
    config = init_config()
    trainer = Trainer(log=log, config=config)