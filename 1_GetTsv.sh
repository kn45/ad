#!/bin/bash

data_raw=data_all/round1_ijcai_18_train_20180301.txt
data_all=data_all/data_all.tsv
cat $data_raw | awk '{if (NR>1) print $0}' | sed -e 's/ /	/g' > $data_all
