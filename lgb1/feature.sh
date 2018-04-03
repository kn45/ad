#!/bin/bash

set -x

# build dict
cat ../data_all/data_all.tsv | python feature_build.py basic_transform > ./feature/data_all_transform.tsv
cat ./feature/data_all_transform.tsv | python feature_build.py build_category_dict | sort | uniq | awk '{print $1"\t"NR}' > ./feature/category_dict

# tranform
cat ../data_train/data_train.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/train_feature.libfm

cat ../data_train/data_valid.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/valid_feature.libfm

cat ../data_test/data_test.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/test_feature.libfm
