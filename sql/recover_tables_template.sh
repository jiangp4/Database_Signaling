#!/bin/bash

cmd_recover="mysql -h cellsig-dev.cocbn4pwa3av.us-east-1.rds.amazonaws.com -P 3306 -u Username -pPassword Database_Signaling"

for table in "$@"
do
    eval "gunzip < ${table} | ${cmd_recover}"
done
