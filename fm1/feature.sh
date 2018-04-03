#!/bin/bash

set -x

# build dict
python feature_build.py build_value_bin ./feature/value_bin
cat ../data_all/data_all.tsv | python feature_build.py value2bin ./feature/value_bin > ./feature/data_all_in_cat.tsv
cat ./feature/data_all_in_cat.tsv | python feature_build.py build_category_dict | sort | uniq | awk '{print $1"\t"NR}' > ./feature/category_dict

# tranform
cat ../data_train/data_trnvld.tsv | python feature_build.py value2bin ./feature/value_bin > ./feature/trnvld_category.tsv
cat ./feature/trnvld_category.tsv | python feature_build.py category2feature ./feature/category_dict > ./feature/feature_trnvld.libfm

