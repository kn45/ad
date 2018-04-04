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
train_feat = 'feature/trnvld_feature.libfm'
test_feat = 'feature/test_feature.libfm'
pred_feat = 'feature/pred_feature.libfm'
all_feat='feature/all_feature.libfm'
pred_res = 'predict/predict_res'


def train(mode):
    logging.info('loading training data')
    if mode == 'a':
        tf = train_feat
    if mode == 'b':
        tf = all_feat
    data_train_dmat = xgb.DMatrix(tf)
    data_valid_dmat = xgb.DMatrix(test_feat)

    logging.info('start training')
    bst_params = {
        'nthread': 8,
        'silent': 1,
        'eta': 0.05,
        'gamma': 1.0,
        'eval_metric': ['logloss'],
        'max_depth': 7,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'objective': 'binary:logistic',
        'min_child_weight': 1,
        'alpha': 1.0,
        'lambda': 1.0}
    train_params = {
        'params': bst_params,
        'dtrain': data_train_dmat,
        'evals': [(data_train_dmat, 'train'), (data_valid_dmat, 'valid_0')],
        'maximize': False,
        'verbose_eval': True}
    if mode == 'a':
        train_params['num_boost_round'] = 1000
        train_params['early_stopping_rounds'] = 100
    if mode == 'b':
        train_params['num_boost_round'] = cPickle.load(open(model_file, 'rb')).best_iteration

    mdl_bst = xgb.train(**train_params)

    logging.info('Saving model')
    # not use save_model mothod because it cannot dump best_iteration etc.
    cPickle.dump(mdl_bst, open(model_file, 'wb'))

    feat_imp = mdl_bst.get_score(importance_type='gain').items()
    print sorted(feat_imp, key=itemgetter(1), reverse=True)[0:10]


def pred():
    resf = open(pred_res, 'w')
    data_pred_dmat = xgb.DMatrix(pred_feat)

    # init gbt
    mdl_bst = cPickle.load(open(model_file, 'rb'))
    print 'best iteration:', mdl_bst.best_iteration
    mdl_bst.set_param('nthread', 1)
    preds = mdl_bst.predict(
        data_pred_dmat,
        ntree_limit=mdl_bst.best_iteration)
    for p in preds:
        print >> resf, p
    resf.close()


if __name__ == '__main__':
    train('a')
    train('b')
    pred()
