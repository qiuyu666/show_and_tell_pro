#!/usr/bin/env bash

export USER=qiuyu
export py2env=/home/dixin/python/py2env/bin/activate
export HOME=/home/${USER}/im2txt/

today_time=$(date --date="0 day" +"%m%d")
yesterday_time=$(date --date="-1 day" +"%m%d")
last_time=$(date --date="-2 day" +"%m%d")
visit_date=$(date --date="0 day" +"%Y%m%d")
last_date=$(date --date="-1 day" +"%Y%m%d")


# Directory containing preprocessed MSCOCO data.
MSCOCO_DIR="/home/qiuyu/zhuye_look_comment_data"
if [ ! -d "${MSCOCO_DIR}" ]; then
  mkdir ${MSCOCO_DIR}
fi
# Inception v3 checkpoint file.
INCEPTION_CHECKPOINT="${HOME}/im2txt/data/inception_v3/inception_v3.ckpt"

# Directory to save the model.
MODEL_DIR="${HOME}/im2txt/zhuye_look_comment_model"



# JPEG image file to caption.
IMAGE_FILE="${HOME}/im2txt/data/mscoco/val2014/COCO_val2014_000000224477.jpg"
cd ${HOME}


is_train=False
steps=200000
gpu=0

#train  stage
# Run the training script.
cd ${HOME}

source ${py2env}
CUDA_VISIBLE_DEVICES=${gpu}  python -m im2txt.train  \
  --input_file_pattern="${MSCOCO_DIR}/tfrecord_data/train-?????-of-00256" \
  --inception_checkpoint_file="${INCEPTION_CHECKPOINT}" \
  --train_dir="${MODEL_DIR}/train" \
  --train_inception=${is_train} \
  --number_of_steps=${steps} \
  --log_every_n_steps=50
#cd  ${HOME}
#source ${py2env}
#evaluate
#CUDA_VISIBLE_DEVICES=${gpu} python -m im2txt.evaluate \
 # --input_file_pattern="${MSCOCO_DIR}/tfrecord_data/val-?????-of-00004" \
  #--checkpoint_dir="${MODEL_DIR}/train" \
  #--eval_dir="${MODEL_DIR}/eval"


#inference stage
# Run inference to generate captions.
#CUDA_VISIBLE_DEVICES=${gpu}  python -m  im2txt.run_inference \
#  --checkpoint_path=${CHECKPOINT_PATH} \
#  --vocab_file=${VOCAB_FILE} \
#  --input_files=${IMAGE_FILE}
