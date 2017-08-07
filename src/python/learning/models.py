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
#   python.learning.models - Machine Learning Model definitions & mappings
#

from importlib import import_module

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

class Model(object):
    """Interface for all machine learning models. Abstracts implementation
        specific model usage into a consistent API.
    """
    def __init__(self, name, package, learning_type, param, log=False):
        """:params:
            name: machine learning model name, in config/models/x.cfg
            package: importable python module for model name (namespace)
            learning_type: supervised, unsupervised, or reinforcement?
            param: parameters relevent to model, also in config/models/x.cfg
        """
        self.log = log
        self.learning_type = str(learning_type)
        self.param = dict(param)
        self.name = str(name)
        self.package = str(package)
        self.model = self.model_loader(name=name, package=package, param=param)

    @property
    def param(self):
        return self.param

    @param.setter
    def param(self, item, value)
        self.param[item] = value

    @staticmethod
    def print(msg, level="debug"):
        """Print method wrapper so that if a logger is passed to init it is used.
        """
        if self.log:
            getattr(self.log, level)(msg)
        else:
            print(msg)

    def model_loader(self, name, package, param):
        """Retrieves model object <name> from <package> with <param>.
        """
        if 'sklearn' in package:
            self.print("Importing {} from {}".format(name, package))
            module = import_module(package, name)
            self.print("Instantiating {}".format(name))
            clf = getattr(module, name)(**param)
            return clf
        else:
            raise Exception("SchemaNotImplemented: {}.{}".format(package, name))