#!/bin/bash

pred_src=../data_all/round1_ijcai_18_test_a_20180301.txt
pred_example=../data_all/round1_ijcai_18_result_demo_20180301.txt

head -1 $pred_example > predict/submit.txt
cat $pred_src | awk -F' ' '{if(NR>1) print $1}' | paste -d' ' - predict/predict_res >> predict/submit.txt
