#!/usr/bin/env bash
USER=qiuyu
export py2env=/home/dixin/python/py2env/bin/activate
export HOME=/home/${USER}

today_time=$(date --date="0 day" +"%m%d")
yesterday_time=$(date --date="-1 day" +"%m%d")
last_time=$(date --date="-2 day" +"%m%d")
visit_date=$(date --date="0 day" +"%Y%m%d")
last_date=$(date --date="-1 day" +"%Y%m%d")

gpu=1$

cd ${HOME}
source ${py2env}
CUDA_VISIBLE_DEVICES=${gpu}  python "${HOME}/im2txt/bin/mgj_bin/similar_textcnn_generate_samples/download_Data.py"                                       
