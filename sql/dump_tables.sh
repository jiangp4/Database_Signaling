#!/bin/bash

cmd_dump="mysqldump --add-drop-table -u peng_jiang -pNCI_PJ_123 Database_Signaling"

for table in Account_account Association_aliasname Association_association Association_gene Association_gene_Alias Association_signal Association_signal_Gene Association_treatment Profiler_taskupload
do
    eval "${cmd_dump} ${table} > ${table}.sql"
done
