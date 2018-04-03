#!/usr/bin/env python

import cPickle
import logging
import numpy as np
import sys
import xgboost as xgb
from operator import itemgetter

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

model_file = 'model/gbt_model.pkl'
trainf = 'feature/train_feature.libfm'
validf = 'feature/valid_feature.libfm'
testf = 'feature/test_feature.libfm'


def train():
    logging.info('loading training data')
    data_train_dmat = xgb.DMatrix(trainf)
    data_valid_dmat = xgb.DMatrix(validf)

    logging.info('start training')
    bst_params = {
        'nthread': 8,
        'silent': 1,
        'eta': 0.05,
        'gamma': 1.0,
        'eval_metric': ['logloss'],
        'max_depth': 7,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'objective': 'binary:logistic',
        'min_child_weight': 10,
        'alpha': 1.0,
        'lambda': 1.0}
    train_params = {
        'params': bst_params,
        'dtrain': data_train_dmat,
        'num_boost_round': 1000,  # max round
        'evals': [(data_train_dmat, 'train'), (data_valid_dmat, 'valid_0')],
        'maximize': False,
        'early_stopping_rounds': 100,
        'verbose_eval': True}
    mdl_bst = xgb.train(**train_params)

    logging.info('Saving model')
    # not use save_model mothod because it cannot dump best_iteration etc.
    cPickle.dump(mdl_bst, open(model_file, 'wb'))

    feat_imp = mdl_bst.get_score(importance_type='gain').items()
    print sorted(feat_imp, key=itemgetter(1), reverse=True)[0:10]


def test():
    resf = open('test_res', 'w')
    data_test_dmat = xgb.DMatrix(testf)

    # init gbt
    mdl_bst = cPickle.load(open(model_file, 'rb'))
    mdl_bst.set_param('nthread', 1)
    mdl_bst.set_param('eval_metric', 'logloss')

    test_metric = mdl_bst.eval_set([(data_test_dmat, 'test_0')])
    print test_metric.split(':')[-1], float(test_metric.split(':')[-1]) ** 2 / 2.
    pred_res = mdl_bst.predict(
        data_test_dmat,
        ntree_limit=mdl_bst.best_iteration)
    for i in pred_res:
        print >> resf, i
    resf.close()


if __name__ == '__main__':
    train()
    #test()
