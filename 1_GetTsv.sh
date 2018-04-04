#!/bin/bash

data_all_raw=data_all/round1_ijcai_18_train_20180301.txt
data_all=data_all/data_all.tsv

data_pred_raw=data_all/round1_ijcai_18_test_a_20180301.txt
data_pred=data_pred/data_pred.tsv


cat $data_all_raw | awk '{if (NR>1) print $0}' | sed -e 's/ /	/g' > $data_all

cat $data_pred_raw | awk '{if (NR>1) print $0}' | sed -e 's/ /	/g' > $data_pred
