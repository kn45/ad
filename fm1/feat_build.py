#!/usr/bin/env python

import sys
sys.path.append('../utils')
from dataproc import BinSpliter, DictTable


feat_cfg = [
    ['instance_id', [0, 'cat']],  # 47w, uniq
    ['item_id', [1, 'cat']], # 1w, medium
    ['item_category_list', [0]],
    ['item_property_list', [0]],
    ['item_brand_id', [1, 'cat']],  # 2056, dense
    ['item_city_id', [1, 'cat']],  # 129, dense
    ['item_price_level', [1, 'value']],  # 14, int
    ['item_sales_level', [1, 'value', -1]],  # 18, int, missing
    ['item_collected_level', [1, 'value']],  # 18, int
    ['item_pv_level', [1, 'value']], # 22, int
    ['user_id', [1, 'cat']],  # 20w, sparse
    ['user_gender_id', [1, 'cat', -1]],  # 3, dense, missing
    ['user_age_level', [1, 'value', -1]],  # 8, int, missing
    ['user_occupation_id', [1, 'cat', -1]],  # 4, dense, missing
    ['user_star_level', [1, 'value', -1]], # 11, int, missing
    ['context_id', [0, 'cat']],  # 47w, uniq
    ['context_timestamp', [0, 'value']],  # 28w, int, in 7-days, take out half-hour?
    ['context_page_id', [1, 'value']],  # 20, int
    ['predict_category_property', [0]],
    ['shop_id', [1, 'cat']],  # 3960, dense
    ['shop_review_num_level', [1, 'value']],  # 26, int
    ['shop_review_positive_rate', [1, 'value', -1]],  # float, missing
    ['shop_star_level', [1, 'value']], # 22, int
    ['shop_score_service', [1, 'value', -1]],  # float, missing
    ['shop_score_delivery', [1, 'value', -1]],  # float, missing
    ['shop_score_description', [1, 'value', -1]],  # float, missing
    ['is_trade', [0]]  # 469117:9021 = 52:1, ratio+ = 
    ]


def build_value_bin():
    data_file = '../data_all/data_all.tsv'
    mbin = BinSpliter()
    for idx, feat in enumerate(feat_cfg):
        if feat[1][0] == 1 and feat[1][1] == 'value':
            with open(data_file) as f:
                data = [float(x.rstrip('\n').split('\t')[idx]) for x in f.readlines()]
                data = [x for x in data if x != -1]
            mbin.add_bin(data, feat[0], 100)
    mbin.save_bin('val_feat_bin')


def build_category_dict():
    for ln in sys.stdin:
        flds = ln.rstrip('\n').split('\t')
        for idx, feat in enumerate(feat_cfg):
            if feat[1][0] == 1:
                if flds[idx] != '-1':
                    print feat[0] + '_' + flds[idx]


def category2feature():
    cat_idx = DictTable('cat_feat_dict')
    for ln in sys.stdin:
        flds = ln.rstrip('\n').split('\t')
        feats = []
        for idx, fld in enumerate(flds):
            if fld == '-1':
                continue
            if feat_cfg[idx][1][0] == 1:
                feats.extend(cat_idx.lookup([feat_cfg[idx][0]+'_'+fld]))
                print feat_cfg[idx][0]+'_'+fld, cat_idx.lookup([feat_cfg[idx][0]+'_'+fld])
        feats = sorted(feats)
        print ' '.join([flds[-1]] + [str(x) + ':1' for x in feats])


def value2bin():
    # transfer value to bin, preserve -1
    bsp = BinSpliter()
    bsp.load_bin('val_feat_bin')
    for ln in sys.stdin:
        flds = ln.rstrip('\n').split('\t')
        for idx, fld in enumerate(flds):
            if fld == '-1':
                continue
            if feat_cfg[idx][1][0] == 1 and feat_cfg[idx][1][1] == 'value':
                num_bin = bsp.find_bin(feat_cfg[idx][0], float(fld))
                flds[idx] = str(num_bin)
        print '\t'.join(flds)


if __name__ == '__main__':
    if sys.argv[1] == 'build_value_bin':
        build_value_bin()
    if sys.argv[1] == 'value2bin':
        value2bin()
    if sys.argv[1] == 'build_category_dict':
        build_category_dict()
    if sys.argv[1] == 'category2feature':
        category2feature()


