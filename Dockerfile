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
#   main Dockerfile - sentience-base
#

# Fetch base image
FROM ubuntu:zesty

MAINTAINER Yazan Obeidi

# Update package manager and install dependencies
RUN apt-get update && apt-get install -y \
    python3.6 \ 
    python3-pip
    
# Create project directory
RUN mkdir /sentience

# Make it default directory i.e. root
WORKDIR /sentience

# Copy project
ADD . /sentience

# Add project to path
ENV PATH=/sentience/:$PATH

# Add project to pythonpath to resolve module imports from src
ENV PYTHONPATH=/sentience/:$PYTHONPATH

# Create configuration directory
RUN mkdir -p /etc/sentience/config

# Export log directory environment variable
ENV SENTIENCE_CONFIG_DIR=/etc/sentience/config

# Copy config
COPY config $SENTIENCE_CONFIG_DIR

# Install Python requirements
RUN pip3 install -r $SENTIENCE_CONFIG_DIR/base_requirements.txt

# Create log directory
RUN mkdir -p /var/sentience/log

# Set log directory environment variable
ENV SENTIENCE_LOG_DIR=/var/sentience/log