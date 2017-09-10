#!/bin/bash
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
#   sentience build script
#
#   Usage: $./build.sh [--dev|--prod]
#

# Get single argument passed
OPT=$1

# Tidy up, make output of rm silent in case it does not exist
rm docker-compose.yml &>/dev/null

case $OPT in
    -h|--help)
        echo "Sentience build script"
        echo "Usage: "
        echo " "
        echo "$./build.sh [depoyment]"
        echo "-d|--dev : development"
        echo "-p|--prod : production"
        ;;
    -d|--dev)
        echo "Building for development"
        cp compose/dev.yml docker-compose.yml
        ;;
    -p|--prod)
        echo "Building for production"
        cp compose/prod.yml docker-compose.yml
        ;;
    *)
    echo "No deployment option specified"
    ;;
esac

# Deploy
docker-compose up --build