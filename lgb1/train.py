#!/usr/bin/env python

import cPickle
import logging
import numpy as np
import sys
import lightgbm as lgb
from operator import itemgetter

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

trainf = 'feature/trnvld_feature.libfm'
#validf = 'feature/valid_feature.libfm'
testf = 'feature/test_feature.libfm'


def train():
    logging.info('loading training data')
    cats = [1, 4, 5, 11, 13, 16, 19]
    data_train_dmat = lgb.Dataset(trainf, categorical_feature=cats)
    data_valid_dmat = lgb.Dataset(testf, categorical_feature=cats)
    #data_test_dmat = lgb.Dataset(testf, categorical_feature=cats)

    print 'data loaded'
    logging.info('start training')
    params = {
        'application': 'binary',
        'num_leaves': 63,
        'max_depth': 7,
        'learning_rate': 0.03,
        'min_data_in_leaf': 10,
        'metric': 'binary_logloss',
        'min_sum_hessian_in_leaf': 1.,
        'lambda_l1': 1.0,
        'lambda_l2': 1.0,
        'feature_fraction': 0.7,
        #'max_bin': 127,
        'bagging_fraction': 0.7
    }

    train_params = {
        'params': params,
        'train_set': data_train_dmat,
        'num_boost_round': 1000,  # max round
        'early_stopping_rounds': 1000,
        'verbose_eval': True,
        'categorical_feature': cats,
        'valid_sets': [data_train_dmat, data_valid_dmat]
    }

    mdl_bst = lgb.train(**train_params)


if __name__ == '__main__':
    train()

