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
#   interactor Docker file
#

# Fetch base image
FROM sentience_sentience-base:latest

# Copy configuration to existing directory
COPY config $SENTIENCE_CONFIG_DIR

# Install Python requirements
# NOTE need to use "python3.6 -m pip" instead of pip3.6 install ... 
# because pip3.6 is not presently included in ubuntu:zesty
RUN python3.6 -m pip install -r $SENTIENCE_CONFIG_DIR/requirements.txt

ENTRYPOINT ["/sentience/interactor/init.sh"]