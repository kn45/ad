#!/bin/bash

#python feat_build.py build_value_bin
#cat ../data_all/data_all.tsv | python feat_build.py value2bin > ./data_all_in_cat.tsv
#cat ./data_all_in_cat.tsv | python feat_build.py build_category_dict | sort | uniq | awk '{print $1"\t"NR}'> cat_feat_dict
cat ../data_train/data_trnvld.tsv | python feat_build.py category2feature > ./feature_trnvld.libfm

