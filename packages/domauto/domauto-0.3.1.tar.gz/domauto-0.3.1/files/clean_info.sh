#!/bin/bash

if [ $# = 0 ]
then
    rm $DOM_AUTOPSY_DIR/files/*_INFO_*RCA.pickle
else
    rm $DOM_AUTOPSY_DIR/files/*_INFO_$1.pickle
fi
