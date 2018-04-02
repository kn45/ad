#!/bin/bash

cat ../data_all/data_all.tsv | python feat_build.py build_category_dict | sort | uniq | awk '{print $1"\t"NR+1}'> cat_feat_dict

python feat_build.py build_value_bin

