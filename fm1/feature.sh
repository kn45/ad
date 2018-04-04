#!/bin/bash

set -x

# build dict
cat ../data_all/data_all.tsv | python feature_build.py basic_transform > ./feature/data_all_transform.tsv
python feature_build.py build_value_bin ./feature/value_bin ./feature/data_all_transform.tsv
cat ./feature/data_all_transform.tsv | python feature_build.py value2bin ./feature/value_bin > ./feature/data_all_in_cat.tsv
cat ./feature/data_all_in_cat.tsv | python feature_build.py build_category_dict | sort | uniq | awk '{print $1"\t"NR}' > ./feature/category_dict

# tranform
cat ../data_train/data_trnvld.tsv | \
python feature_build.py basic_transform | \
python feature_build.py value2bin ./feature/value_bin | \
python feature_build.py category2feature ./feature/category_dict > ./feature/trnvld_feature.libfm

cat ../data_test/data_test.tsv | \
python feature_build.py basic_transform | \
python feature_build.py value2bin ./feature/value_bin | \
python feature_build.py category2feature ./feature/category_dict > ./feature/test_feature.libfm

cat ../data_all/data_all.tsv | \
python feature_build.py basic_transform | \
python feature_build.py value2bin ./feature/value_bin | \
python feature_build.py category2feature ./feature/category_dict > ./feature/test_feature.libfm
