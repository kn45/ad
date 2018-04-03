#!/bin/bash

set -x

# tranform
cat ../data_train/data_trnvld.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/trnvld_feature.libfm

<<!
cat ../data_train/data_valid.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/valid_feature.libfm
!

cat ../data_test/data_test.tsv | \
python feature_build.py basic_transform | \
python feature_build.py category2feature ./feature/category_dict > ./feature/test_feature.libfm
