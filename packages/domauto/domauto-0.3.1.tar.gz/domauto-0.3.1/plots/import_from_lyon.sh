#!/bin/bash

if [ $# -eq 0 ]
then
    TOKEN="*"
else
    TOKEN=$1
fi

scp -r jseneca@cca.in2p3.fr:/sps/km3net/users/jseneca/aanet/dom_autopsy/plots/"$TOKEN" .
