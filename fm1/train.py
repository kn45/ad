#!/usr/bin/env python


import numpy as np
import sys
import tensorflow as tf
sys.path.append('../utils')
import dataproc
from fm import FMClassifier

INP_DIM = 214444
HID_DIM = 256
REG_W = 0.0  # 1st
REG_V = 0.0  # 2nd

LR = 1e-4
TOTAL_ITER = 10000
MAX_EPOCH = 20

MDL_CKPT_DIR = './model/model.ckpt'
TRAIN_FILE = 'feature/trnvld_feature.libfm'
TEST_FILE = 'feature/test_feature.libfm'
PRED_FILE = 'feature/pred_feature.libfm'


def inp_fn(data):
    bs = len(data)
    x_idx = []
    x_vals = []
    y_vals = []
    for i, inst in enumerate(data):
        flds = inst.split(' ')
        label = float(flds[0])
        feats = flds[1:]
        for feat in feats:
            idx, val = feat.split(':')
            idx = int(idx) - 1  # libsvm starts from 1
            val = float(val)
            x_idx.append([i, idx])
            x_vals.append(val)
        y_vals.append([label])
    x_shape = [bs, INP_DIM]
    return (x_idx, x_vals, x_shape), y_vals


freader = dataproc.BatchReader(TRAIN_FILE, max_epoch=MAX_EPOCH)
with open(TEST_FILE) as ftest:
    test_data = [x.rstrip('\n') for x in ftest.readlines()]
test_x, test_y = inp_fn(test_data)

mdl = FMClassifier(
    inp_dim=INP_DIM,
    hid_dim=HID_DIM,
    lambda_w=REG_W,
    lambda_v=REG_V,
    lr=LR)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())
niter = 0

while niter < TOTAL_ITER:
    niter += 1
    batch_data = freader.get_batch(256)
    if not batch_data:
        break
    train_x, train_y = inp_fn(batch_data)
    mdl.train_step(sess, train_x, train_y)
    train_eval = mdl.eval_step(sess, train_x, train_y)
    test_eval = mdl.eval_step(sess, test_x, test_y) \
        if niter % 20 == 0 else 'SKIP'
    print niter, 'train:', train_eval, 'test:', test_eval
save_path = mdl.saver.save(sess, MDL_CKPT_DIR, global_step=mdl.global_step)
print "model saved:", save_path


"""
# pred
with open(PRED_FILE) as fpred:
    pred_data = [x.rstrip('\n') for x in fpred.readlines()]
pred_x, pred_y = inp_fn(pred_data)
with open('pred_res.csv', 'w') as f:
    preds = mdl.predict(sess, pred_x)
    for p in preds:
        print >> f, p[0]
"""

sess.close()
